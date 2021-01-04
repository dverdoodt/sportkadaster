<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 10:54:48 2020

@author: dverdoodt
@description: Laucnh the creation of a report, based on the API provided by the sportkadaster.
https://api-web-sportbrussels.dev.voxteneo.com/swagger/index.html

-	Dev : https://api-web-sportbrussels.dev.voxteneo.com/swagger/index.html
-	Staging : http://staging.manager.sport.brussels/api/swagger/index.html
-	Prod : http://manager.sport.brussels/api/swagger/index.html


In the first sheet of an Excel file, the requested reports are flagged.
Based on this "request", an Excel report is created based 
on the information from the API of the sportkadaster

Write report generation date in the name of the Excel file.

"""
# =========================================
# Import modules
# =========================================
import pandas as pd
import sportkadaster_api_tools as api_tools
from datetime import datetime
from configparser import ConfigParser


# =========================================
# Read config-file
# =========================================
config_object = ConfigParser()
config_object.read('config.ini')

config_parameters = config_object["staging"]  ## development | staging | production

# Read connection info from config file
END_POINT = config_parameters["END_POINT"]
API_KEY = config_parameters["API_KEY"]


# =========================================
# Set parameters
# excel writer output file
# =========================================
# Define Excel output file
output_file = 'dashboard_sportkadaster_{0}.xlsx'.format(datetime.now().strftime("%Y%m%d"))
print("Excel output file is: {0}".format(output_file))

# =========================================
# Prepare header API request
# =========================================
headers = {
    'accept': 'application/json',
    'Authorization': API_KEY,
    'Content-Type': 'application/json'
}

# =========================================
# Dashboard
# =========================================

# =========================================
# Subsides
# 
# subsidies	                      All subsidies available in the sportkadaster
# subsidies_subsidisingPartner	   Subsidies grouped by subsidising partner. This is the partner that grants(gives) the subsidy
# subsidies_organisation	         Subsidies grouped by organisation that receives the subsidy
# =========================================
request_body = api_tools.makeRequestbodySubsidy()    
df_subsidies = api_tools.getSubsidies(END_POINT, headers, request_body)
df_subsidies['creationYear'] = pd.DatetimeIndex(df_subsidies['creationDate']).year

## Add organisation name to the subsidies dataframe
df_organisations = pd.DataFrame(columns=['organisationMainId', 'organisationName'])
# Itereer niet over alle subsidies, maar over alle unieke organisaties die een subsidie ontvangen.
for organisationMainId in df_subsidies['organisationMainId'].unique():
    ## Subsidies are granted to organisations flagged as 'clubs' and organsations flagged as 'not-a-club'.
    ## Clubs
    request_body = api_tools.makeRequestBodyOrganisation(organisationId=organisationMainId, status='V', isClub=True)
    df_organisation = api_tools.getOrganisations(END_POINT, headers, request_body)
    if len(df_organisation) == 1:
        # print('isClub: ')
        translatedName = df_organisation['translatedName'][0]
    else: 
        translatedName = None
        
    ## No Clubs (juridical organisation)
    request_body = api_tools.makeRequestBodyOrganisation(organisationId=organisationMainId, status='V', isClub=False)
    df_organisation = api_tools.getOrganisations(END_POINT, headers, request_body)
    if len(df_organisation) == 1:
        # print('is not a club (juridical organisation): ')
        translatedName = df_organisation['translatedName'][0]
    else:
        translatedName = None
        
    # Add organisationName to the the organisationId
    df_organisations = df_organisations.append(
        {'organisationMainId': organisationMainId,
         'organisationName': translatedName},
        ignore_index=True)


## Merge dataframes df_subsidies and df_organisations based on organisationId. Sort based on the partner and the creationDate
df_subsidies = pd.merge(df_subsidies, df_organisations, how='left', on='organisationMainId')
df_subsidies = df_subsidies.sort_values(by=['subsidisingPartner', 'creationDate'], ascending=[True, False])

## Group by subsidisingPartner
df_subsidies_subsidisingPartner = df_subsidies.groupby(['subsidisingPartner', 'creationYear'], as_index=False).sum(['amount'])
df_subsidies_subsidisingPartner = df_subsidies_subsidisingPartner.drop(['id'], axis=1)
df_subsidies_subsidisingPartner = df_subsidies_subsidisingPartner.sort_values(by=['subsidisingPartner', 'creationYear'], ascending=[True, False])

## Group by organisation
df_subsidies_organisation = df_subsidies.groupby(['organisationMainId', 'organisationName', 'creationYear'], as_index=False).sum(['amount'])
df_subsidies_organisation = df_subsidies_organisation.drop(['id'], axis=1)
df_subsidies_organisation = df_subsidies_organisation.sort_values(by=['organisationName', 'creationYear'], ascending=[True, False])

with pd.ExcelWriter(output_file, mode='w') as writer:
    df_subsidies.to_excel(writer, sheet_name='subsidies', index=False, freeze_panes=(1,0))
    df_subsidies_organisation.to_excel(writer, sheet_name='subsidies_organisation', index=False, freeze_panes=(1,0))
    df_subsidies_subsidisingPartner.to_excel(writer, sheet_name='subsidies_subsidisingPartner', index=False, freeze_panes=(1,0))


# =========================================
# Organisation
#
#	organisation	                         All organisations (clubs and juridical organisations)	
#	organisation_legalStatus	            Organisations per juridical status	
#	organisation_organisationType	      Organisation per club type	
# =========================================
# Get both clubs and non-clubs (juridical organiations)"
request_body = api_tools.makeRequestBodyOrganisation()
df_organisations_isClub = api_tools.getOrganisations(END_POINT, headers, request_body)
df_organisations_isClub = df_organisations_isClub[df_organisations_isClub["status"] == 'V']

request_body = api_tools.makeRequestBodyOrganisation(isClub=False)
df_organisations_isNotClub = api_tools.getOrganisations(END_POINT, headers, request_body)
df_organisations_isNotClub = df_organisations_isNotClub[df_organisations_isNotClub["status"] == 'V']

# concatenate organisations: clubs and non-clubs
df_organisations = pd.concat([df_organisations_isClub, df_organisations_isNotClub], ignore_index=True)


## Map organisationActivities to organisationActivitiesValues
# Dictionary with activities
request_body = api_tools.makeRequestBodyActivity()
df_activities = api_tools.getActivities(END_POINT, headers, request_body)
dict_activities = df_activities.set_index('id')['translatedName'].to_dict()

# Create an empty list to store the activities
organisationActivities = []
for index, organisation in df_organisations.iterrows():
    organisationId = organisation['id']
    # use a dictionary to map the items in the list of activities
    newList = [dict_activities.get(activityId, None) for activityId in organisation['organisationActivities']]
    #print('{0}: {1}'.format(organisationId, newList))
    organisationActivities.append([organisationId, newList])

# Convert list to dataframe
df_organisationActivities = pd.DataFrame(data=organisationActivities, columns=['id', 'organisationActivitiesValues'])

# Merge dataframe to the organisations
df_organisations = pd.merge(df_organisations, df_organisationActivities, how='left', on=['id'])


## Map organisationActivitiesAudiences to organisationActivitiesAudiencesValues
# Dictionary with audiences
request_body = api_tools.makeRequestBodyAudience()
df_audiences= api_tools.getAudiences(END_POINT, headers, request_body)
dict_audiences = df_audiences.set_index('id')['translatedName'].to_dict()

# Create an empty list to store the activityAudiences
organisationActivitiesAudiences = []
for index, organisation in df_organisations.iterrows():
    organisationId = organisation['id']
    # use a dictionary to map the items in the list of activities
    newList = [dict_audiences.get(audienceId, None) for audienceId in organisation['organisationActivitiesAudiences']]
    #print('{0}: {1}'.format(organisationId, newList))
    organisationActivitiesAudiences.append([organisationId, newList])

# Convert list to dataframe
df_organisationActivitiesAudiences = pd.DataFrame(data=organisationActivitiesAudiences, columns=['id', 'organisationActivitiesAudiencesValues'])

# Merge dataframe to the organisations
df_organisations = pd.merge(df_organisations, df_organisationActivitiesAudiences, how='left', on=['id'])


## Sort df_organisations by name ascending
df_organisations = df_organisations.sort_values(by=['translatedName'], ascending=True)


## Group by legalStatus
df_organisations_legalStatus = df_organisations.groupby(['legalStatus'], as_index=False).size()
df_organisations_legalStatus = df_organisations_legalStatus.rename(columns={"size": "count"})
df_organisations_legalStatus = df_organisations_legalStatus.sort_values(by=['legalStatus', 'count'], ascending=[True, False])


## Group by organisationTypeName (most of them are still empty at this moment)
df_organisations_organisationType = df_organisations.groupby(['organisationTypeName'], as_index=False).size()
df_organisations_organisationType = df_organisations_organisationType.rename(columns={"size": "count"})
df_organisations_organisationType = df_organisations_organisationType.sort_values(by=['organisationTypeName', 'count'], ascending=[True, False])


with pd.ExcelWriter(output_file, mode='a') as writer:    
    df_organisations.to_excel(writer, sheet_name='organisations', index=False, freeze_panes=(1,0))
    df_organisations_legalStatus.to_excel(writer, sheet_name='organisations_legalStatus', index=False, freeze_panes=(1,0))
    df_organisations_organisationType.to_excel(writer, sheet_name='organisations_organisationType', index=False, freeze_panes=(1,0))

# =========================================
# Facility: GetFacilityType
# =========================================
request_body = api_tools.makeRequestBodyFacilityType()

# Launch API request
df_facilityTypes = api_tools.getFacilityTypes(END_POINT, headers, request_body)

with pd.ExcelWriter(output_file, mode='a') as writer:
    df_facilityTypes.to_excel(writer, sheet_name='facilityTypes', index=False, freeze_panes=(1,0))


# =========================================
# Infrastructure
# infrastructures

# =========================================
request_body = api_tools.makeRequestBodyInfrastructure(lastModificationDate="2020-01-01T00:00:00")
df_infrastructures = api_tools.getInfrastructures(END_POINT, headers, request_body)

# places (details_inPlaceID)
# Organisation names (organisations)
# Club names (clubs)
# Facilities (facilities)

# Dictionaries
# places
request_body = api_tools.makeRequestBodyPlaces(language='en')
df_places = api_tools.getPlaces(END_POINT, headers, request_body)
dict_places = df_places.set_index('id')['nameFr'].to_dict()

# organisations and clubs
request_body = api_tools.makeRequestBodyOrganisation(isClub=False)
df_organisations_nonClubs = api_tools.getOrganisations(END_POINT, headers, request_body)
df_organisations_nonClubs = df_organisations_nonClubs[df_organisations_nonClubs["status"] == 'V']

request_body = api_tools.makeRequestBodyOrganisation(isClub=True)
df_organisations_clubs = api_tools.getOrganisations(END_POINT, headers, request_body)
df_organisations_clubs = df_organisations_clubs[df_organisations_clubs["status"] == 'V']

# concatenate organisations: clubs and non-clubs and make dictionary
df_organisations = pd.concat([df_organisations_nonClubs, df_organisations_clubs], ignore_index=True)
dict_organisations = df_organisations.set_index('id')['translatedName'].to_dict()

# Empty lists to store the places, organisations, clubs, facilities
organisations = []
clubs = []
facility_names = []
facility_facilityTypeId = []
facility_facilityTypeName = []
facility_accessiblePRM = []
places = []

for index, infrastructure in df_infrastructures.iterrows():
    #infrastructureId = infrastructure['id'] ## Hier niet zeker of Id of mainId te gebruiken.
    infrastructureId = infrastructure['mainId']

    # organisations and clubs
    if not infrastructure['organisations'] == None:
        organisationsNameList = [dict_organisations.get(organisationId, None) for organisationId in infrastructure['organisations']]
    else:
        organisationsNameList = None
    organisations.append([infrastructureId, organisationsNameList])
    
    if not infrastructure['clubs'] == None:
        clubsNameList = [dict_organisations.get(clubId, None) for clubId in infrastructure['clubs']]
    else:
        clubsNameList = None
    clubs.append([infrastructureId, clubsNameList])

    # facilities
    request_body = api_tools.makeRequestBodyFacility(infrastructureMainId=infrastructureId)
    df_facility = api_tools.getFacilities(END_POINT, headers, request_body)
    
    tmplist_facilityNames = []
    tmplist_facilityTypeIds = []
    tmplist_facilityTypeNames = []
    tmplist_facilityAccessiblePMR = []
    for jindex, facility in df_facility.iterrows():
        tmplist_facilityNames.append(facility['name'])
        tmplist_facilityTypeIds.append(facility['facilityTypeId'])
        tmplist_facilityTypeNames.append(facility['facilityTypeName'])
        tmplist_facilityAccessiblePMR.append(facility['accessiblePRM'])
            
    facility_names.append([infrastructureId, tmplist_facilityNames])
    facility_facilityTypeId.append([infrastructureId, tmplist_facilityTypeIds])
    facility_facilityTypeName.append([infrastructureId, tmplist_facilityTypeNames])
    facility_accessiblePRM.append([infrastructureId, tmplist_facilityAccessiblePMR])

    # places
    places.append([infrastructureId, dict_places.get(infrastructure['details_inPlaceId'], None)])
        
    
# Convert lists to dataframes
df_infraOrganisations = pd.DataFrame(data=organisations, columns=['id', 'infraOrganisations'])
df_infraClubs = pd.DataFrame(data=clubs, columns=['id', 'infraClubs'])
df_infraFacilityNames = pd.DataFrame(data=facility_names, columns=['id', 'infraFacilityNames'])
df_infraFacilityTypeIds = pd.DataFrame(data=facility_facilityTypeId, columns=['id', 'infraFacilityTypeIds'])
df_infraFacilityTypeNames = pd.DataFrame(data=facility_facilityTypeName, columns=['id', 'infraFacilityTypeNames'])
df_infraFacilityAccessiblePRM = pd.DataFrame(data=facility_accessiblePRM, columns=['id', 'infraFacilityAccessiblePRM'])
df_infraPlaces = pd.DataFrame(data=places, columns=['id', 'infraPlaces'])

# Merge dataframes to the organisations
df_infrastructures = df_infrastructures.merge(df_infraOrganisations, how='left', on=['id'])
df_infrastructures = df_infrastructures.merge(df_infraClubs, how='left', on=['id'])
df_infrastructures = df_infrastructures.merge(df_infraFacilityNames, how='left', on=['id'])
df_infrastructures = df_infrastructures.merge(df_infraFacilityTypeIds, how='left', on=['id'])
df_infrastructures = df_infrastructures.merge(df_infraFacilityTypeNames, how='left', on=['id'])
df_infrastructures = df_infrastructures.merge(df_infraFacilityAccessiblePRM, how='left', on=['id'])
df_infrastructures = df_infrastructures.merge(df_infraPlaces, how='left', on=['id'])

with pd.ExcelWriter(output_file, mode='a') as writer:
    df_infrastructures.to_excel(writer, sheet_name='infrastructures', index=False, freeze_panes=(1,0))


# =========================================
# Place
# places
# =========================================
request_body = api_tools.makeRequestBodyPlaces(language='en')
df_places = api_tools.getPlaces(END_POINT, headers, request_body)

with pd.ExcelWriter(output_file, mode='a') as writer:
    df_places.to_excel(writer, sheet_name='places', index=False, freeze_panes=(1,0))
    

# =========================================
# Event
# 
#
# =========================================
## request_body = api_tools.makeRequestBodyEvents(eventMainId='81129f5f-581a-4bcc-bba5-1a202e0428d4', language='en', isRegular=True)
request_body = api_tools.makeRequestBodyEvents(language='en', isRegular=True, status='V')
df_events_regular = api_tools.getEvents(END_POINT, headers, request_body)

## request_body = api_tools.makeRequestBodyEvents(eventMainId='1ff76e5f-ad86-4a70-9934-aedfebd428cc', language='en', isRegular=False)
request_body = api_tools.makeRequestBodyEvents(language='en', isRegular=False, status='V')
df_events_irregular = api_tools.getEvents(END_POINT, headers, request_body)

# Concatenate regular and irregular events.
df_events = pd.concat([df_events_regular, df_events_irregular], ignore_index=True)

## Loop over de activities en de audiences en voeg deze toe aan de dataframe als een extra kolom
## Zoek de overeenkomstige activities en audiences op via een dictionary.

## Map activities to activitiesValues
# Dictionary with activities
request_body = api_tools.makeRequestBodyActivity(language='en')
df_activities = api_tools.getActivities(END_POINT, headers, request_body)
dict_activities = df_activities.set_index('id')['translatedName'].to_dict()

# Create an empty list to store the activities
eventActivities = []
for index, event in df_events.iterrows():
    eventId = event['id']
    # use a dictionary to map the items in the list of events
    newList = [dict_activities.get(eventId, None) for eventId in event['eventActivities']]
    eventActivities.append([eventId, newList])

# Convert list to dataframe
df_eventActivities = pd.DataFrame(data=eventActivities, columns=['id', 'activitiesValues'])

# Merge dataframe to the organisations
df_events = pd.merge(df_events, df_eventActivities, how='left', on=['id'])


## Map audiences to audiencesValues
# Dictionary with audiences
request_body = api_tools.makeRequestBodyAudience(language='en')
df_audiences = api_tools.getAudiences(END_POINT, headers, request_body)
dict_audiences = df_audiences.set_index('id')['translatedName'].to_dict()

# Create an empty list to store the audiences
eventAudiences = []
for index, event in df_events.iterrows():
    eventId = event['id']
    # use a dictionary to map the items in the list of events
    newList = [dict_audiences.get(eventId, None) for eventId in event['eventAudiences']]
    eventAudiences.append([eventId, newList])

# Convert list to dataframe
df_eventAudiences = pd.DataFrame(data=eventAudiences, columns=['id', 'audiencesValues'])

# Merge dataframe to the organisations
df_events = pd.merge(df_events, df_eventAudiences, how='left', on=['id'])


with pd.ExcelWriter(output_file, mode='a') as writer:    
    df_events.to_excel(writer, sheet_name='events', index=False, freeze_panes=(1,0))
    
    

# =========================================
# Activity
# De verschillende sport activiteiten die zijn geregistreerd in het sportkadaster.
# Als je "0" ingeeft voor "page" of "id" wordt er niet gefilterd, en worden alle resultaten weergegeven.
# Als "name" bij activity filter een lege string komt overeen met de null-waarde.
# =========================================
request_body = api_tools.makeRequestBodyActivity()
## Launch API request
df_activities = api_tools.getActivities(END_POINT, headers, request_body)
df_mainActivities = api_tools.getMainActivities(END_POINT, headers, request_body)
with pd.ExcelWriter(output_file, mode='a') as writer:    
    df_activities.to_excel(writer, sheet_name='activities', index=False, freeze_panes=(1,0))
    df_mainActivities.to_excel(writer, sheet_name='mainActivities', index=False, freeze_panes=(1,0))
        

# =========================================
# Audience
# Doelpublieken
# =========================================
request_body = api_tools.makeRequestBodyAudience()
## Launch API request
df_audiences = api_tools.getAudiences(END_POINT, headers, request_body)
with pd.ExcelWriter(output_file, mode='a') as writer:    
    df_audiences.to_excel(writer, sheet_name='audiences', index=False, freeze_panes=(1,0))

=======
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 10:54:48 2020

@author: dverdoodt
@description: Laucnh the creation of a report, based on the API provided by the sportkadaster.
https://api-web-sportbrussels.dev.voxteneo.com/swagger/index.html

-	Dev : https://api-web-sportbrussels.dev.voxteneo.com/swagger/index.html
-	Staging : http://staging.manager.sport.brussels/api/swagger/index.html
-	Prod : http://manager.sport.brussels/api/swagger/index.html


In the first sheet of an Excel file, the requested reports are flagged.
Based on this "request", an Excel report is created based 
on the information from the API of the sportkadaster

Write report generation date in the name of the Excel file.

"""
# =========================================
# Import modules
# =========================================
import pandas as pd
import sportkadaster_api_tools as api_tools
from datetime import datetime
from configparser import ConfigParser


# =========================================
# Read config-file
# =========================================
config_object = ConfigParser()
config_object.read('config.ini')

config_parameters = config_object["staging"]  ## development | staging | production

# Read connection info from config file
END_POINT = config_parameters["END_POINT"]
API_KEY = config_parameters["API_KEY"]


# =========================================
# Set parameters
# excel writer output file
# =========================================
# Define Excel output file
output_file = 'dashboard_sportkadaster_{0}.xlsx'.format(datetime.now().strftime("%Y%m%d"))
print("Excel output file is: {0}".format(output_file))

# =========================================
# Prepare header API request
# =========================================
headers = {
    'accept': 'application/json',
    'Authorization': API_KEY,
    'Content-Type': 'application/json'
}

# =========================================
# Dashboard
# =========================================

# =========================================
# Subsides
# 
# subsidies	                      All subsidies available in the sportkadaster
# subsidies_subsidisingPartner	   Subsidies grouped by subsidising partner. This is the partner that grants(gives) the subsidy
# subsidies_organisation	         Subsidies grouped by organisation that receives the subsidy
# =========================================
request_body = api_tools.makeRequestbodySubsidy()    
df_subsidies = api_tools.getSubsidies(END_POINT, headers, request_body)
df_subsidies['creationYear'] = pd.DatetimeIndex(df_subsidies['creationDate']).year

## Add organisation name to the subsidies dataframe
df_organisations = pd.DataFrame(columns=['organisationMainId', 'organisationName'])
# Itereer niet over alle subsidies, maar over alle unieke organisaties die een subsidie ontvangen.
for organisationMainId in df_subsidies['organisationMainId'].unique():
    ## Subsidies are granted to organisations flagged as 'clubs' and organsations flagged as 'not-a-club'.
    ## Clubs
    request_body = api_tools.makeRequestBodyOrganisation(organisationId=organisationMainId, status='V', isClub=True)
    df_organisation = api_tools.getOrganisations(END_POINT, headers, request_body)
    if len(df_organisation) == 1:
        # print('isClub: ')
        translatedName = df_organisation['translatedName'][0]
    else: 
        translatedName = None
        
    ## No Clubs (juridical organisation)
    request_body = api_tools.makeRequestBodyOrganisation(organisationId=organisationMainId, status='V', isClub=False)
    df_organisation = api_tools.getOrganisations(END_POINT, headers, request_body)
    if len(df_organisation) == 1:
        # print('is not a club (juridical organisation): ')
        translatedName = df_organisation['translatedName'][0]
    else:
        translatedName = None
        
    # Add organisationName to the the organisationId
    df_organisations = df_organisations.append(
        {'organisationMainId': organisationMainId,
         'organisationName': translatedName},
        ignore_index=True)


## Merge dataframes df_subsidies and df_organisations based on organisationId. Sort based on the partner and the creationDate
df_subsidies = pd.merge(df_subsidies, df_organisations, how='left', on='organisationMainId')
df_subsidies = df_subsidies.sort_values(by=['subsidisingPartner', 'creationDate'], ascending=[True, False])

## Group by subsidisingPartner
df_subsidies_subsidisingPartner = df_subsidies.groupby(['subsidisingPartner', 'creationYear'], as_index=False).sum(['amount'])
df_subsidies_subsidisingPartner = df_subsidies_subsidisingPartner.drop(['id'], axis=1)
df_subsidies_subsidisingPartner = df_subsidies_subsidisingPartner.sort_values(by=['subsidisingPartner', 'creationYear'], ascending=[True, False])

## Group by organisation
df_subsidies_organisation = df_subsidies.groupby(['organisationMainId', 'organisationName', 'creationYear'], as_index=False).sum(['amount'])
df_subsidies_organisation = df_subsidies_organisation.drop(['id'], axis=1)
df_subsidies_organisation = df_subsidies_organisation.sort_values(by=['organisationName', 'creationYear'], ascending=[True, False])

with pd.ExcelWriter(output_file, mode='w') as writer:
    df_subsidies.to_excel(writer, sheet_name='subsidies', index=False, freeze_panes=(1,0))
    df_subsidies_organisation.to_excel(writer, sheet_name='subsidies_organisation', index=False, freeze_panes=(1,0))
    df_subsidies_subsidisingPartner.to_excel(writer, sheet_name='subsidies_subsidisingPartner', index=False, freeze_panes=(1,0))


# =========================================
# Organisation
#
#	organisation	                         All organisations (clubs and juridical organisations)	
#	organisation_legalStatus	            Organisations per juridical status	
#	organisation_organisationType	      Organisation per club type	
# =========================================
# Get both clubs and non-clubs (juridical organiations)"
request_body = api_tools.makeRequestBodyOrganisation()
df_organisations_isClub = api_tools.getOrganisations(END_POINT, headers, request_body)
df_organisations_isClub = df_organisations_isClub[df_organisations_isClub["status"] == 'V']

request_body = api_tools.makeRequestBodyOrganisation(isClub=False)
df_organisations_isNotClub = api_tools.getOrganisations(END_POINT, headers, request_body)
df_organisations_isNotClub = df_organisations_isNotClub[df_organisations_isNotClub["status"] == 'V']

# concatenate organisations: clubs and non-clubs
df_organisations = pd.concat([df_organisations_isClub, df_organisations_isNotClub], ignore_index=True)


## Map organisationActivities to organisationActivitiesValues
# Dictionary with activities
request_body = api_tools.makeRequestBodyActivity()
df_activities = api_tools.getActivities(END_POINT, headers, request_body)
dict_activities = df_activities.set_index('id')['translatedName'].to_dict()

# Create an empty list to store the activities
organisationActivities = []
for index, organisation in df_organisations.iterrows():
    organisationId = organisation['id']
    # use a dictionary to map the items in the list of activities
    newList = [dict_activities.get(activityId, None) for activityId in organisation['organisationActivities']]
    #print('{0}: {1}'.format(organisationId, newList))
    organisationActivities.append([organisationId, newList])

# Convert list to dataframe
df_organisationActivities = pd.DataFrame(data=organisationActivities, columns=['id', 'organisationActivitiesValues'])

# Merge dataframe to the organisations
df_organisations = pd.merge(df_organisations, df_organisationActivities, how='left', on=['id'])


## Map organisationActivitiesAudiences to organisationActivitiesAudiencesValues
# Dictionary with audiences
request_body = api_tools.makeRequestBodyAudience()
df_audiences= api_tools.getAudiences(END_POINT, headers, request_body)
dict_audiences = df_audiences.set_index('id')['translatedName'].to_dict()

# Create an empty list to store the activityAudiences
organisationActivitiesAudiences = []
for index, organisation in df_organisations.iterrows():
    organisationId = organisation['id']
    # use a dictionary to map the items in the list of activities
    newList = [dict_audiences.get(audienceId, None) for audienceId in organisation['organisationActivitiesAudiences']]
    #print('{0}: {1}'.format(organisationId, newList))
    organisationActivitiesAudiences.append([organisationId, newList])

# Convert list to dataframe
df_organisationActivitiesAudiences = pd.DataFrame(data=organisationActivitiesAudiences, columns=['id', 'organisationActivitiesAudiencesValues'])

# Merge dataframe to the organisations
df_organisations = pd.merge(df_organisations, df_organisationActivitiesAudiences, how='left', on=['id'])


## Sort df_organisations by name ascending
df_organisations = df_organisations.sort_values(by=['translatedName'], ascending=True)


## Group by legalStatus
df_organisations_legalStatus = df_organisations.groupby(['legalStatus'], as_index=False).size()
df_organisations_legalStatus = df_organisations_legalStatus.rename(columns={"size": "count"})
df_organisations_legalStatus = df_organisations_legalStatus.sort_values(by=['legalStatus', 'count'], ascending=[True, False])


## Group by organisationTypeName (most of them are still empty at this moment)
df_organisations_organisationType = df_organisations.groupby(['organisationTypeName'], as_index=False).size()
df_organisations_organisationType = df_organisations_organisationType.rename(columns={"size": "count"})
df_organisations_organisationType = df_organisations_organisationType.sort_values(by=['organisationTypeName', 'count'], ascending=[True, False])


with pd.ExcelWriter(output_file, mode='a') as writer:    
    df_organisations.to_excel(writer, sheet_name='organisations', index=False, freeze_panes=(1,0))
    df_organisations_legalStatus.to_excel(writer, sheet_name='organisations_legalStatus', index=False, freeze_panes=(1,0))
    df_organisations_organisationType.to_excel(writer, sheet_name='organisations_organisationType', index=False, freeze_panes=(1,0))

# =========================================
# Facility: GetFacilityType
# =========================================
request_body = api_tools.makeRequestBodyFacilityType()

# Launch API request
df_facilityTypes = api_tools.getFacilityTypes(END_POINT, headers, request_body)

with pd.ExcelWriter(output_file, mode='a') as writer:
    df_facilityTypes.to_excel(writer, sheet_name='facilityTypes', index=False, freeze_panes=(1,0))


# =========================================
# Infrastructure
# infrastructures

# =========================================
request_body = api_tools.makeRequestBodyInfrastructure(lastModificationDate="2020-01-01T00:00:00")
df_infrastructures = api_tools.getInfrastructures(END_POINT, headers, request_body)

# places (details_inPlaceID)
# Organisation names (organisations)
# Club names (clubs)
# Facilities (facilities)

# Dictionaries
# places
request_body = api_tools.makeRequestBodyPlaces(language='en')
df_places = api_tools.getPlaces(END_POINT, headers, request_body)
dict_places = df_places.set_index('id')['nameFr'].to_dict()

# organisations and clubs
request_body = api_tools.makeRequestBodyOrganisation(isClub=False)
df_organisations_nonClubs = api_tools.getOrganisations(END_POINT, headers, request_body)
df_organisations_nonClubs = df_organisations_nonClubs[df_organisations_nonClubs["status"] == 'V']

request_body = api_tools.makeRequestBodyOrganisation(isClub=True)
df_organisations_clubs = api_tools.getOrganisations(END_POINT, headers, request_body)
df_organisations_clubs = df_organisations_clubs[df_organisations_clubs["status"] == 'V']

# concatenate organisations: clubs and non-clubs and make dictionary
df_organisations = pd.concat([df_organisations_nonClubs, df_organisations_clubs], ignore_index=True)
dict_organisations = df_organisations.set_index('id')['translatedName'].to_dict()

# Empty lists to store the places, organisations, clubs, facilities
organisations = []
clubs = []
facility_names = []
facility_facilityTypeId = []
facility_facilityTypeName = []
facility_accessiblePRM = []
places = []

for index, infrastructure in df_infrastructures.iterrows():
    #infrastructureId = infrastructure['id'] ## Hier niet zeker of Id of mainId te gebruiken.
    infrastructureId = infrastructure['mainId']

    # organisations and clubs
    if not infrastructure['organisations'] == None:
        organisationsNameList = [dict_organisations.get(organisationId, None) for organisationId in infrastructure['organisations']]
    else:
        organisationsNameList = None
    organisations.append([infrastructureId, organisationsNameList])
    
    if not infrastructure['clubs'] == None:
        clubsNameList = [dict_organisations.get(clubId, None) for clubId in infrastructure['clubs']]
    else:
        clubsNameList = None
    clubs.append([infrastructureId, clubsNameList])

    # facilities
    request_body = api_tools.makeRequestBodyFacility(infrastructureMainId=infrastructureId)
    df_facility = api_tools.getFacilities(END_POINT, headers, request_body)
    
    tmplist_facilityNames = []
    tmplist_facilityTypeIds = []
    tmplist_facilityTypeNames = []
    tmplist_facilityAccessiblePMR = []
    for jindex, facility in df_facility.iterrows():
        tmplist_facilityNames.append(facility['name'])
        tmplist_facilityTypeIds.append(facility['facilityTypeId'])
        tmplist_facilityTypeNames.append(facility['facilityTypeName'])
        tmplist_facilityAccessiblePMR.append(facility['accessiblePRM'])
            
    facility_names.append([infrastructureId, tmplist_facilityNames])
    facility_facilityTypeId.append([infrastructureId, tmplist_facilityTypeIds])
    facility_facilityTypeName.append([infrastructureId, tmplist_facilityTypeNames])
    facility_accessiblePRM.append([infrastructureId, tmplist_facilityAccessiblePMR])

    # places
    places.append([infrastructureId, dict_places.get(infrastructure['details_inPlaceId'], None)])
        
    
# Convert lists to dataframes
df_infraOrganisations = pd.DataFrame(data=organisations, columns=['id', 'infraOrganisations'])
df_infraClubs = pd.DataFrame(data=clubs, columns=['id', 'infraClubs'])
df_infraFacilityNames = pd.DataFrame(data=facility_names, columns=['id', 'infraFacilityNames'])
df_infraFacilityTypeIds = pd.DataFrame(data=facility_facilityTypeId, columns=['id', 'infraFacilityTypeIds'])
df_infraFacilityTypeNames = pd.DataFrame(data=facility_facilityTypeName, columns=['id', 'infraFacilityTypeNames'])
df_infraFacilityAccessiblePRM = pd.DataFrame(data=facility_accessiblePRM, columns=['id', 'infraFacilityAccessiblePRM'])
df_infraPlaces = pd.DataFrame(data=places, columns=['id', 'infraPlaces'])

# Merge dataframes to the organisations
df_infrastructures = df_infrastructures.merge(df_infraOrganisations, how='left', on=['id'])
df_infrastructures = df_infrastructures.merge(df_infraClubs, how='left', on=['id'])
df_infrastructures = df_infrastructures.merge(df_infraFacilityNames, how='left', on=['id'])
df_infrastructures = df_infrastructures.merge(df_infraFacilityTypeIds, how='left', on=['id'])
df_infrastructures = df_infrastructures.merge(df_infraFacilityTypeNames, how='left', on=['id'])
df_infrastructures = df_infrastructures.merge(df_infraFacilityAccessiblePRM, how='left', on=['id'])
df_infrastructures = df_infrastructures.merge(df_infraPlaces, how='left', on=['id'])

with pd.ExcelWriter(output_file, mode='a') as writer:
    df_infrastructures.to_excel(writer, sheet_name='infrastructures', index=False, freeze_panes=(1,0))


# =========================================
# Place
# places
# =========================================
request_body = api_tools.makeRequestBodyPlaces(language='en')
df_places = api_tools.getPlaces(END_POINT, headers, request_body)

with pd.ExcelWriter(output_file, mode='a') as writer:
    df_places.to_excel(writer, sheet_name='places', index=False, freeze_panes=(1,0))
    

# =========================================
# Event
# 
#
# =========================================
## request_body = api_tools.makeRequestBodyEvents(eventMainId='81129f5f-581a-4bcc-bba5-1a202e0428d4', language='en', isRegular=True)
request_body = api_tools.makeRequestBodyEvents(language='en', isRegular=True, status='V')
df_events_regular = api_tools.getEvents(END_POINT, headers, request_body)

## request_body = api_tools.makeRequestBodyEvents(eventMainId='1ff76e5f-ad86-4a70-9934-aedfebd428cc', language='en', isRegular=False)
request_body = api_tools.makeRequestBodyEvents(language='en', isRegular=False, status='V')
df_events_irregular = api_tools.getEvents(END_POINT, headers, request_body)

# Concatenate regular and irregular events.
df_events = pd.concat([df_events_regular, df_events_irregular], ignore_index=True)

## Loop over de activities en de audiences en voeg deze toe aan de dataframe als een extra kolom
## Zoek de overeenkomstige activities en audiences op via een dictionary.

## Map activities to activitiesValues
# Dictionary with activities
request_body = api_tools.makeRequestBodyActivity(language='en')
df_activities = api_tools.getActivities(END_POINT, headers, request_body)
dict_activities = df_activities.set_index('id')['translatedName'].to_dict()

# Create an empty list to store the activities
eventActivities = []
for index, event in df_events.iterrows():
    eventId = event['id']
    # use a dictionary to map the items in the list of events
    newList = [dict_activities.get(eventId, None) for eventId in event['eventActivities']]
    eventActivities.append([eventId, newList])

# Convert list to dataframe
df_eventActivities = pd.DataFrame(data=eventActivities, columns=['id', 'activitiesValues'])

# Merge dataframe to the organisations
df_events = pd.merge(df_events, df_eventActivities, how='left', on=['id'])


## Map audiences to audiencesValues
# Dictionary with audiences
request_body = api_tools.makeRequestBodyAudience(language='en')
df_audiences = api_tools.getAudiences(END_POINT, headers, request_body)
dict_audiences = df_audiences.set_index('id')['translatedName'].to_dict()

# Create an empty list to store the audiences
eventAudiences = []
for index, event in df_events.iterrows():
    eventId = event['id']
    # use a dictionary to map the items in the list of events
    newList = [dict_audiences.get(eventId, None) for eventId in event['eventAudiences']]
    eventAudiences.append([eventId, newList])

# Convert list to dataframe
df_eventAudiences = pd.DataFrame(data=eventAudiences, columns=['id', 'audiencesValues'])

# Merge dataframe to the organisations
df_events = pd.merge(df_events, df_eventAudiences, how='left', on=['id'])


with pd.ExcelWriter(output_file, mode='a') as writer:    
    df_events.to_excel(writer, sheet_name='events', index=False, freeze_panes=(1,0))
    
    

# =========================================
# Activity
# De verschillende sport activiteiten die zijn geregistreerd in het sportkadaster.
# Als je "0" ingeeft voor "page" of "id" wordt er niet gefilterd, en worden alle resultaten weergegeven.
# Als "name" bij activity filter een lege string komt overeen met de null-waarde.
# =========================================
request_body = api_tools.makeRequestBodyActivity()
## Launch API request
df_activities = api_tools.getActivities(END_POINT, headers, request_body)
df_mainActivities = api_tools.getMainActivities(END_POINT, headers, request_body)
with pd.ExcelWriter(output_file, mode='a') as writer:    
    df_activities.to_excel(writer, sheet_name='activities', index=False, freeze_panes=(1,0))
    df_mainActivities.to_excel(writer, sheet_name='mainActivities', index=False, freeze_panes=(1,0))
        

# =========================================
# Audience
# Doelpublieken
# =========================================
request_body = api_tools.makeRequestBodyAudience()
## Launch API request
df_audiences = api_tools.getAudiences(END_POINT, headers, request_body)
with pd.ExcelWriter(output_file, mode='a') as writer:    
    df_audiences.to_excel(writer, sheet_name='audiences', index=False, freeze_panes=(1,0))

>>>>>>> 567c5cacad6c62a5948e7bb89ce6a8acfdd5d0f3
    