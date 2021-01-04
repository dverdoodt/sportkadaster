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
config_object.read(r'C:/Users/dverdoodt/Documents/sportkadaster_api/config.ini')

config_parameters = config_object["staging"]  ## development | staging | production

# Read connection info from config file
END_POINT = config_parameters["END_POINT"]
API_KEY = config_parameters["API_KEY"]


# =========================================
# Set parameters
# excel writer output file
# =========================================
# Define Excel output file
output_file = 'report_sportkadaster_{0}.xlsx'.format(datetime.now().strftime("%Y%m%d"))
print("Excel output file is: {0}".format(output_file)	)

# =========================================
# Prepare header API request
# =========================================
headers = {
    'accept': 'application/json',
    'Authorization': API_KEY,
    'Content-Type': 'application/json'
}

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


# =========================================
# Audience
# Doelpublieken
# =========================================
request_body = api_tools.makeRequestBodyAudience()

## Launch API request
df_audiences = api_tools.getAudiences(END_POINT, headers, request_body)


# =========================================
# Event
# =========================================
## Launch API request
request_body = api_tools.makeRequestBodyEvents(isRegular=True)
df_events_regular = api_tools.getEvents(END_POINT, headers, request_body)

request_body = api_tools.makeRequestBodyEvents(isRegular=False)
df_events_irregular = api_tools.getEvents(END_POINT, headers, request_body)

# =========================================
# Facility: GetFacilityType
# =========================================
request_body = api_tools.makeRequestBodyFacilityType()

# Launch API request
df_facilityTypes = api_tools.getFacilityTypes(END_POINT, headers, request_body)


# =========================================
# Infrastructure
# =========================================
request_body = api_tools.makeRequestBodyInfrastructure()

# Launch API Request
df_infrastructures = api_tools.getInfrastructures(END_POINT, headers, request_body)


# =========================================
# Organisation
# Hoe kunnen de datums gebruikt worden om de organisaties te filteren?
# =========================================
request_body = api_tools.makeRequestBodyOrganisation()

# Launch API Request
df_organisations = api_tools.getOrganisations(END_POINT, headers, request_body)


# =========================================
# Place
# sample: id=0a3c4f9c-651d-458e-83c7-b0899b2c69bb
# =========================================
request_body = api_tools.makeRequestBodyPlaces()

# Launch API Request
df_places = api_tools.getPlaces(END_POINT, headers, request_body)


# =========================================
# Subsidy
# =========================================
request_body = api_tools.makeRequestbodySubsidy()

# Launch API Request
df_subsidies = api_tools.getSubsidies(END_POINT, headers, request_body)


# =========================================
# Facility: GetFacilities
## 504 Gateway time out >> Too many features requested.

## facility met infrastructure main id: 00145419-44b6-4d9a-acef-716efe1474e2 (Dev) of 005f4d42-fdce-4f9a-8821-eb45e50252ce (staging)
#" implementeren zodra infrastructure en Organisation op punt staan.
# Moet gebruik worden in combinatie met een infrstructureMainId en OrganisationMainId"
# =========================================
request_body = api_tools.makeRequestBodyFacility(infrastructureMainId='005f4d42-fdce-4f9a-8821-eb45e50252ce')

# Launch API Request
df_facilities = api_tools.getFacilities(END_POINT, headers, request_body)


# =========================================
# Write to Excel file
# =========================================
with pd.ExcelWriter(output_file) as writer:  
    # Activity
    df_activities.to_excel(writer, sheet_name='activities', index=False, freeze_panes=(1,0))
    df_mainActivities.to_excel(writer, sheet_name='mainactivities', index=False, freeze_panes=(1,0))
    
    # Audience
    df_audiences.to_excel(writer, sheet_name='audiences', index=False, freeze_panes=(1,0))
    
    # Event
    df_events_regular.to_excel(writer, sheet_name='events_regular', index=False, freeze_panes=(1,0))
    df_events_irregular.to_excel(writer, sheet_name='events_irregular', index=False, freeze_panes=(1,0))

    # Facility
    df_facilityTypes.to_excel(writer, sheet_name='facilityTypes', index=False, freeze_panes=(1,0))
    df_facilities.to_excel(writer, sheet_name='facilities', index=False, freeze_panes=(1,0))
    
    # Infrastructure
    df_infrastructures.to_excel(writer, sheet_name='infrastructures', index=False, freeze_panes=(1,0))
    
    
    # Organisation
    df_organisations.to_excel(writer, sheet_name='organisations', index=False, freeze_panes=(1,0))
    
    # Place
    df_places.to_excel(writer, sheet_name='places', index=False, freeze_panes=(1,0))
    
    # Subsidy
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
config_object.read(r'C:/Users/dverdoodt/Documents/sportkadaster_api/config.ini')

config_parameters = config_object["staging"]  ## development | staging | production

# Read connection info from config file
END_POINT = config_parameters["END_POINT"]
API_KEY = config_parameters["API_KEY"]


# =========================================
# Set parameters
# excel writer output file
# =========================================
# Define Excel output file
output_file = 'report_sportkadaster_{0}.xlsx'.format(datetime.now().strftime("%Y%m%d"))
print("Excel output file is: {0}".format(output_file)	)

# =========================================
# Prepare header API request
# =========================================
headers = {
    'accept': 'application/json',
    'Authorization': API_KEY,
    'Content-Type': 'application/json'
}

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


# =========================================
# Audience
# Doelpublieken
# =========================================
request_body = api_tools.makeRequestBodyAudience()

## Launch API request
df_audiences = api_tools.getAudiences(END_POINT, headers, request_body)


# =========================================
# Event
# =========================================
## Launch API request
request_body = api_tools.makeRequestBodyEvents(isRegular=True)
df_events_regular = api_tools.getEvents(END_POINT, headers, request_body)

request_body = api_tools.makeRequestBodyEvents(isRegular=False)
df_events_irregular = api_tools.getEvents(END_POINT, headers, request_body)

# =========================================
# Facility: GetFacilityType
# =========================================
request_body = api_tools.makeRequestBodyFacilityType()

# Launch API request
df_facilityTypes = api_tools.getFacilityTypes(END_POINT, headers, request_body)


# =========================================
# Infrastructure
# =========================================
request_body = api_tools.makeRequestBodyInfrastructure()

# Launch API Request
df_infrastructures = api_tools.getInfrastructures(END_POINT, headers, request_body)


# =========================================
# Organisation
# Hoe kunnen de datums gebruikt worden om de organisaties te filteren?
# =========================================
request_body = api_tools.makeRequestBodyOrganisation()

# Launch API Request
df_organisations = api_tools.getOrganisations(END_POINT, headers, request_body)


# =========================================
# Place
# sample: id=0a3c4f9c-651d-458e-83c7-b0899b2c69bb
# =========================================
request_body = api_tools.makeRequestBodyPlaces()

# Launch API Request
df_places = api_tools.getPlaces(END_POINT, headers, request_body)


# =========================================
# Subsidy
# =========================================
request_body = api_tools.makeRequestbodySubsidy()

# Launch API Request
df_subsidies = api_tools.getSubsidies(END_POINT, headers, request_body)


# =========================================
# Facility: GetFacilities
## 504 Gateway time out >> Too many features requested.

## facility met infrastructure main id: 00145419-44b6-4d9a-acef-716efe1474e2 (Dev) of 005f4d42-fdce-4f9a-8821-eb45e50252ce (staging)
#" implementeren zodra infrastructure en Organisation op punt staan.
# Moet gebruik worden in combinatie met een infrstructureMainId en OrganisationMainId"
# =========================================
request_body = api_tools.makeRequestBodyFacility(infrastructureMainId='005f4d42-fdce-4f9a-8821-eb45e50252ce')

# Launch API Request
df_facilities = api_tools.getFacilities(END_POINT, headers, request_body)


# =========================================
# Write to Excel file
# =========================================
with pd.ExcelWriter(output_file) as writer:  
    # Activity
    df_activities.to_excel(writer, sheet_name='activities', index=False, freeze_panes=(1,0))
    df_mainActivities.to_excel(writer, sheet_name='mainactivities', index=False, freeze_panes=(1,0))
    
    # Audience
    df_audiences.to_excel(writer, sheet_name='audiences', index=False, freeze_panes=(1,0))
    
    # Event
    df_events_regular.to_excel(writer, sheet_name='events_regular', index=False, freeze_panes=(1,0))
    df_events_irregular.to_excel(writer, sheet_name='events_irregular', index=False, freeze_panes=(1,0))

    # Facility
    df_facilityTypes.to_excel(writer, sheet_name='facilityTypes', index=False, freeze_panes=(1,0))
    df_facilities.to_excel(writer, sheet_name='facilities', index=False, freeze_panes=(1,0))
    
    # Infrastructure
    df_infrastructures.to_excel(writer, sheet_name='infrastructures', index=False, freeze_panes=(1,0))
    
    
    # Organisation
    df_organisations.to_excel(writer, sheet_name='organisations', index=False, freeze_panes=(1,0))
    
    # Place
    df_places.to_excel(writer, sheet_name='places', index=False, freeze_panes=(1,0))
    
    # Subsidy
>>>>>>> 567c5cacad6c62a5948e7bb89ce6a8acfdd5d0f3
    df_subsidies.to_excel(writer, sheet_name='subsidies', index=False, freeze_panes=(1,0))