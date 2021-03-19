# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 14:11:04 2020

@author: dverdoodt
@ tools for the sportkadaster API

"""
import requests
import json
import pandas as pd
from datetime import datetime

########################################################
###   make request bodies
########################################################
def makeRequestBodyActivity(language='fr', activityId=0, name=""):
    """
    Returns
    -------
    dict: request body for the subsidy API.
    """
    request_body = {
      "request": {
        "filter": {
          "language": language,
          "page": 0,
          "itemsPerPage": 10
        },
        "activityFilter": {
          "id": activityId,
          "name": name
        }
      }
    }
    return request_body


def makeRequestbodySubsidy(language='fr', subsidyId=0, subsidyOrganisation='', status='',lastModificationDate=None):
    """
    returns the request body (dictionary) for the subsidy API
    """
    request_body = {
      "request": {
        "filter": {
          "language": language,
          "page": 0,
          "itemsPerPage": 0
        },
        "subsidyFilter": {
          "id": subsidyId,
          "subsidyOrganization": subsidyOrganisation,
          "status": status,
          "lastModificationDate": lastModificationDate
        }
      }
    }
    return request_body

def makeRequestBodyOrganisation(language='fr', organisationId=None, organisationMainId=None, 
                                name='', shortName='', partOfTheName='', status= '', 
                                referenceKey='', companyNumber='', organizationType='',
                                startDate=None, endDate=None, lastModificationDate=None, 
                                publish=True,
                                showDetails=True, showPeople=True, showOrganizationActivities=True, 
                                showInfrastructures=True, showPlaces=True, showChildOrganizations=True, 
                                isClub=True):
    """
    Returns
    -------
    dict: request body for the subsidy API.
    """
    request_body = {
      "request": {
        "generalFilter": {
          "language": language,
          "page": 0,
          "itemsPerPage": 0
        },
        "organisationFilter": {
          "id": organisationId,
          "mainId": organisationMainId,
          "name": name,
          "shortName": shortName,
          "partOfTheName": partOfTheName,
          "status": status,
          "referenceKey": referenceKey,
          "companyNumber": companyNumber,
          "organizationType": organizationType,
          "startDate": startDate,
          "endDate": endDate,
          "lastModificationDate": lastModificationDate,
          "publish": publish
        },
        "showDetails": showDetails,
        "showPeople": showPeople,
        "showOrganizationActivities": showOrganizationActivities,
        "showInfrastructures": showInfrastructures,
        "showPlaces": showPlaces,
        "showChildOrganizations": showChildOrganizations,
        "isClub": isClub
      }
    }
    return request_body

def makeRequestBodyAudience(language='fr', audienceId=0, audienceName=""):
    request_body = {
      "request": {
        "filter": {
          "language": language,
          "page": 0,
          "itemsPerPage": 0
        },
        "audienceFilter": {
          "id": audienceId,
          "name": audienceName
        }
      }
    }
    return request_body

def makeRequestBodyEvents(language='fr', eventId=None, eventMainId=None, 
                          name="", status="", referenceKey="", 
                          organisationMainId=None, isRegular=True, 
                          publish=True, lastModificationDate="2020-01-01T00:00:00", 
                          showDetails=True, showActivities=True, showAudience=True):
    request_body = {
      "request": {
        "filter": {
          "language": language,
          "page": 1,
          "itemsPerPage": 10
        },
        "eventFilter": {
          "id": eventId,
          "mainId": eventMainId,
          "name": name,
          "status": status,
          "referenceKey": referenceKey,
          "organizationMainId": organisationMainId,
          "isRegular": isRegular,
          "publish": publish,
          "lastModificationDate": lastModificationDate
        },
        "showDetails": showDetails,
        "showActivities": showActivities,
        "showAudience": showAudience
      }
    }
    return request_body

def makeRequestBodyFacilityType(language='fr', facilityTypeId=0, facilityTypeName=""):
    request_body = {
      "request": {
        "filter": {
          "language": language,
          "page": 0,
          "itemsPerPage": 0
        },
        "facilityTypeFilter": {
          "id": facilityTypeId,
          "name": facilityTypeName
        }
      }
    }
    return request_body

def makeRequestBodyFacility(language='fr', facilityId=None, facilityMainId=None, 
                            name="", status="", referenceKey="", infrastructureMainId=None, 
                            organizationMainId=None, facilityType="", lastModificationDate="2020-01-01T00:00:00",
                            showDetails=True, showActivity=True, showFacilityTypeValues=True):
    request_body = {
      "request": {
        "filter": {
          "language": language,
          "page": 0,
          "itemsPerPage": 0
        },
        "facilityFilter": {
          "id": facilityId,
          "mainId": facilityMainId,
          "name": name,
          "status": status,
          "referenceKey": referenceKey,
          "infrastrucutreMainId": infrastructureMainId,
          "organizationMainId": organizationMainId,
          "facilityType": facilityType,
          "lastModificationDate": lastModificationDate
        },
        "showDetails": showDetails,
        "showActivity": showActivity,
        "showFacilityTypeValues": showFacilityTypeValues
      }
    }
    return request_body

def makeRequestBodyPlaces(language='en', placeId=None, placeMainId=None, 
                          name='', status='', addressPostalCode='', 
                          lastModificationDate=None, publish=True, 
                          showDetails=True, showProperties=True, 
                          showOrganisations=True, showInfrastructures=True):
    request_body = {
      "request": {
        "filter": {
          "language": language,
          "page": 0,
          "itemsPerPage": 0
        },
        "placeFilter": {
          "id": placeId,
          "mainId": placeMainId,
          "name": name,
          "status": status,
          "addressPostalCode": addressPostalCode,
          "lastModificationDate": lastModificationDate,
          "publish": publish
        },
        "showDetails": showDetails,
        "showProperties": showProperties,
        "showOrganisations": showOrganisations,
        "showInfrastructures": showInfrastructures
      }
    }
    return request_body

def makeRequestBodyInfrastructure(language='fr', infrastructureId=None, infrastructureMainId=None,
                                  name="", status="", referenceKey="", publish=True, 
                                  lastModificationDate="2020-01-01T00:00:00", 
                                  showDetails=True, showOrganisations=True, 
                                  showClubs=True, showFacilities=True, 
                                  showProperties=True, showImages=True):
    request_body = {
      "request": {
        "filter": {
          "language": language,
          "page": 0,
          "itemsPerPage": 0
        },
        "infrastructureFilter": {
          "id": infrastructureId,
          "mainId": infrastructureMainId,
          "name": name,
          "status": status,
          "referenceKey": referenceKey,
          "publish": publish,
          "lastModificationDate": lastModificationDate
        },
        "showDetails": showDetails,
        "showOrganisations": showOrganisations,
        "showClubs": showClubs,
        "showFacilities": showFacilities,
        "showProperties": showProperties,
        "showImages": showImages
      }
    }
    return request_body
      
def getActivities(end_point, headers, request_body):
    """
    Parameters
    ----------
    end_point : string
        API URL endpoint
    headers : dictionary
        headers, connection details
    request_body : dictionary
        data to pass to the API request to filter the data

    Returns
    -------
    activities : Nested list: Id, ParentId, TranslatedName
    """
    url = end_point + '/api/Activity/GetActivities'
    
    # Launch API Call
    response = requests.post(url, headers=headers, data=json.dumps(request_body))
        
    # Format response into a list
    activities_extended_list = response.json()['response']
    activities = []
    # append header names
    activities.append(['id', 'parentId', 'translatedName'])
    for i, activity in enumerate(activities_extended_list):
        activities.append([activity['id'], activity['parentId'], activity['translatedName']])
        
    # Convert to pandas dataframe
    df_activities = pd.DataFrame(activities[1:], columns=activities[0])

    return df_activities
        
def getMainActivities(end_point, headers, request_body):
    """
    Parameters
    ----------
    end_point : string
        API URL endpoint
    headers : dictionary
        headers, connection details
    request_body : dictionary
        data to pass to the API request to filter the data

    Returns
    -------
    activities : Nested list: Id, ParentId, TranslatedName
    """
    url = end_point + '/api/Activity/GetActivities'
    
    # Launch API Call
    response = requests.post(url, headers=headers, data=json.dumps(request_body))
        
    # Format response into a list
    mainActivities_extended_list = response.json()['response']
    mainActivities = []
    # append header names
    mainActivities.append(['id', 'parentId', 'translatedName'])
    for i, mainActivity in enumerate(mainActivities_extended_list):
        # Main activities do not have a parentId
        if mainActivity['parentId'] == None:
            mainActivities.append([mainActivity['id'], mainActivity['parentId'], mainActivity['translatedName']])
            
   # Convert to pandas dataframe
    df_mainActivities = pd.DataFrame(mainActivities[1:], columns=mainActivities[0])

    return df_mainActivities

def getAudiences(end_point, headers, request_body):
    """
    Parameters
    ----------
    end_point : string
        API URL endpoint
    headers : dictionary
        headers, connection details
    request_body : dictionary
        data to pass to the API request to filter the data

    Returns
    -------
    audiences - Dataframe: id, name, translatedName, minAge, maxAge, disabled, gender, type
    """
    url = end_point + '/api/Audience/GetAudiences'
    
    # Launch API Call
    response = requests.post(url, headers=headers, data=json.dumps(request_body))
        
    # Format response into a list
    audiences_extended_list = response.json()['response']
    audiences = []
    # append header names
    audiences.append(['id', 'name', 'translatedName', 'minAge', 'maxAge', 'disabled', 'gender', 'type'])
    for i, audience in enumerate(audiences_extended_list):
        audiences.append(
            [audience['id'],
             audience['name'], 
             audience['translatedName'], 
             audience['minAge'],
             audience['maxAge'],
             audience['disabled'],
             audience['gender'],
             audience['type']
             ])
        
    # Convert to pandas dataframe
    df_audiences = pd.DataFrame(audiences[1:], columns=audiences[0])
    
    return df_audiences

def getEvents(end_point, headers, request_body):
    """
    Parameters
    ----------
    end_point : string
        API URL endpoint
    headers : dictionary
        headers, connection details
    request_body : dictionary
        data to pass to the API request to filter the data

    Returns
    -------
    events - Nested list
    """
    url = end_point + '/api/Event/GetEvents'
    
    # Launch API Call
    response = requests.post(url, headers=headers, data=json.dumps(request_body))
    
    # Format response into a list
    events_extended_list = response.json()['response']
    ##print(events_extended_list)
    #print('')
    events = []
    # append header names
    events.append(['id', 'isVisibleOnWebsite', 'activityType', 'status',  
                   # name and description
                   'name', 'description', 
                   # location - extra infos
                   'placeMainId',
                   'place', 
                   # details
                   'isPublic', 'isCompetitive', 'isEntertaining', 'isFree',
                   'fares', 'dayWeek', 'startDate', 'startTime', 'endDate', 'endTime',
                   'isRegular',
                   'eventActivities', 'eventAudiences',
                   'eventLanguages',               
                   # Contact info
                   'organiser', 
                   'surname', 'firstname',  
                   
                   'organisation', 'organiserPeople', 
                   'mail','website'
                   ])
        
    for i, event in enumerate(events_extended_list):
        # languages
        
        if not event['details']['eventLang'] == None:
            languageList = [language['translatedUsedLanguage'] for language in event['details']['eventLang']]
        else: 
            languageList = None
            
        if not event['basicInfo'] == None:
            events.append(
                [event['basicInfo']['id'], # id in URL. eventId
                 event['basicInfo']['publish'], # isVisibleOnWebsite
                 event['basicInfo']['translatedType'], # activityType
                 event['details']['status'],
                 
                 event['details']['eventLg'][0]['name'],
                 event['details']['eventLg'][0]['description'],
                 
                 event['details']['placeMainId'],
                 event['details']['eventLg'][0]['place'], # location - extra infos
                 
                 event['details']['public'], # isPublic
                 event['details']['competitive'], # isCompetitive
                 event['details']['entertaining'], # isEntertaining
                 event['details']['free'], # isFree
    
                 event['details']['eventLg'][0]['fares'],
                 event['details']['timetable'][0]['dayWeek'],
                 stringToDate(event['details']['timetable'][0]['start']),
                 stringToTime(event['details']['timetable'][0]['start']),
                 stringToDate(event['details']['timetable'][0]['end']),
                 stringToTime(event['details']['timetable'][0]['end']),

                 event['details']['isRegular'],
                 
                 event['eventActivity'],
                 event['eventAudience'],
                 languageList,
    
                 event['details']['eventLg'][0]['organiser'],
                 
                 event['details']['contact']['name'],
                 event['details']['contact']['firstname'],
    
                 event['details']['organisation'],
                 event['details']['organiserPeople'],
                 event['details']['mail'],
                 event['details']['website'],
    
                 ])
        
    # Convert to pandas dataframe
    df_events = pd.DataFrame(events[1:], columns=events[0])

    return df_events

def getFacilityTypes(end_point, headers, request_body):
    """
    Parameters
    ----------
    end_point : string
        API URL endpoint
    headers : dictionary
        headers, connection details
    request_body : dictionary
        data to pass to the API request to filter the data

    Returns
    -------
    audiences - Nested list
    """
    url = end_point + '/api/Facility/GetFacilityType'
    
    # Launch API Call
    response = requests.post(url, headers=headers, data=json.dumps(request_body))
        
    # Format response into a list
    facilityTypes_extended_list = response.json()['response']
    facilityTypes = []
    # append header names
    facilityTypes.append(['id', 'translatedName', 'status', 'facilityTypes'])

    facilityTypeDict = {'R':'Radio button', 'C':'Check boxes', 'F':'Text fields', 
                        'M':'Comment field', 'S':'Drop down', 'T': 'Time', 
                        'D':'Date', 'I':'Integer', 'A':'Disciplines', 'H': 'Title'
                        }
    for i, facilityType in enumerate(facilityTypes_extended_list):
        # facilityTypeField
        # facilityTypeFields = ''
        # for element in facilityType['facilityTypeField']:
        #    facilityTypeFields += '{0}; '.format(element['name'])
        facilityTypeFields = []
        facilityTypeName = [element['name'] for element in facilityType['facilityTypeField']]
        
        facilityTypeValues = [element['valueType'] for element in facilityType['facilityTypeField']] # datatype
        facilityTypeValues = [facilityTypeDict.get(x, x) for x in facilityTypeValues]
        
        facilityTypeMandatory = [element['mandatory'] for element in facilityType['facilityTypeField']]
        facilityTypeMandatory = ['*' if x == True else '' for x in facilityTypeMandatory]
        
        for i, element in enumerate(facilityTypeName):
            facilityTypeFields.append(element + facilityTypeMandatory[i] + '(' + facilityTypeValues[i] +')')

        facilityTypes.append(
             [facilityType['id'],
              facilityType['translatedName'], 
              facilityType['status'],
              facilityTypeFields #name + mandatory + (type)
              ])
        
    # Convert to pandas dataframe
    df_facilityTypes = pd.DataFrame(facilityTypes[1:], columns=facilityTypes[0])
    return df_facilityTypes

def getInfrastructures(end_point, headers, request_body):
    """
    Parameters
    ----------
    end_point : string
        API URL endpoint
    headers : dictionary
        headers, connection details
    request_body : dictionary
        data to pass to the API request to filter the data

    Returns
    -------
    events - Nested list
    """
    url = end_point + '/api/Infrastructure/GetInfrastructures'
    
    # Launch API Call
    response = requests.post(url, headers=headers, data=json.dumps(request_body))
        
    # Format response into a list
    infrastructures_extended_list = response.json()['response']
    ## print(infrastructures_extended_list)
    infrastructures = []
    # append header names
    infrastructures.append(['id', 'mainId', 'referenceKey', 'name',
                            'organisations',
                            'clubs',
                            'facilities',
                            'status',
                            'details_automatedExternalDefibrillator',
                            'details_energyFile',
                            'details_inPlaceId',
                            'infrastructureProperties'])
    
    for i, infrastructure in enumerate(infrastructures_extended_list):
        # infrastructureName
        if not infrastructure['basicInfo']['infrastructureLg'] == None:
            infrastructureName = infrastructure['basicInfo']['infrastructureLg'][0]['name']
            # this is redundant, because only one value for each language.
            # infrastructureName = [language['name'] for language in infrastructure['basicInfo']['infrastructureLg']]
        else:
            infrastructureName == None
        
        if not infrastructure['infrastructureProperties'] == None:
            infraList = []
            for infra in infrastructure['infrastructureProperties']:
                ## Concatenate number, translatedLabel and type|trasnlatedLabel, if not null-values
                number = xstr(infra['number'])
                translatedLabel1 = xstr(infra['translatedLabel'])
                translatedLabel2 = xstr(infra['type']['translatedLabel'])
                infraList.append('{0} {1} {2}'.format(translatedLabel1, translatedLabel2, number))
            infrastructureProperties = '; '.join(infraList)
            
        else:
            infrastructureProperties == None
        
        infrastructures.append(
            [infrastructure['basicInfo']['id'],
             infrastructure['basicInfo']['mainId'],
             infrastructure['basicInfo']['referenceKey'],
             infrastructureName,
             infrastructure['organisations'],
             infrastructure['clubs'], 
             infrastructure['facilities'],
             infrastructure['details']['status'],
             infrastructure['details']['automatedExternalDefibrillator'],
             infrastructure['details']['energyFile'],
             infrastructure['details']['inPlaceId'],
             infrastructureProperties
             ])
        
    # Convert to pandas dataframe
    df_infrastructures = pd.DataFrame(infrastructures[1:], columns=infrastructures[0])

    return df_infrastructures

def getOrganisations(end_point, headers, request_body):
    """
    Parameters
    ----------
    end_point : string
        API URL endpoint
    headers : dictionary
        headers, connection details
    request_body : dictionary
        data to pass to the API request to filter the data

    Returns
    -------
    events - Nested list
    """
    url = end_point + '/api/Organisation/GetOrganisations'
    
    # Launch API Call
    response = requests.post(url, headers=headers, data=json.dumps(request_body))
        
    # Format response into a list
    organisations_extended_list = response.json()['response']
    
    # Subsidy status organisations
    status_dict = {'N':'Non-Profit Organisation', 'U':'Unincorporated organisation', 'E':'Enterprise', 'P':'Public institution', None:'Undefined'}
    
    
    organisations = []
    # append header names
    organisations.append(['id', 'nameEn', 'nameFr', 'nameNl',
                          'status',
                          'descriptionEn', 'descriptionFr', 'descriptionNl',
                          'infraManager', 'isClub',
                          'type name', 'subtype name', 'subtype info',
                          'reference key', 'companyNumber', 'vat', 'legalName', 'legalStatus',
                          'contact name', 'contact title', 'contact email', 'contact phone',
                          'infrastructures', 
                          'places', 
                          'organisationActivities', 
                          'organisationActivitiesAudiences'])
    
    for i, organisation in enumerate(organisations_extended_list):
        # print(json.dumps(organisation, indent=2))
        
        # type and subtype
        typeName = None
        subTypeName = None
        subTypeInfo = None
        if not organisation['details']['organisationType'] == None:
            ## Club Type = Associated counties
            if not organisation['details']['organisationType']['type'] == None: 
                typeName = organisation['details']['organisationType']['type']['categoryBase']
                subTypeName = organisation['details']['organisationType']['translatedTypeName']
                subTypeInfo = None
            ## Club Type = County
            if not organisation['details']['organisationType']['city'] == None: 
                typeName = organisation['details']['organisationType']['city']['categoryBase']
                subTypeName = organisation['details']['organisationType']['translatedCityName']
                subTypeInfo = organisation['details']['organisationType']['translatedTypeName']
            ## Club Type = Community
            if not organisation['details']['organisationType']['community'] == None: 
                typeName = organisation['details']['organisationType']['community']['categoryBase']
                subTypeName = organisation['details']['organisationType']['translatedCommunityName']
                subTypeInfo = None
                
            if not organisation['details']['organisationType']['level'] == None: 
                typeName = organisation['details']['organisationType']['level']['categoryBase']
                subTypeName = organisation['details']['organisationType']['translatedLevelName']
                subTypeInfo = None
                
            ## Club Type = Schools
            if not organisation['details']['organisationType']['network'] == None: 
                typeName = organisation['details']['organisationType']['network']['categoryBase']
                subTypeName = organisation['details']['organisationType']['translatedNetworkName']
                subTypeInfo = organisation['details']['organisationType']['translatedLevelName'] + ' - ' + organisation['details']['organisationType']['translatedTypeName']
            ## Club Type = Brussels Capital Region
            if not organisation['details']['organisationType']['service'] == None: 
                typeName = organisation['details']['organisationType']['service']['categoryBase']
                subTypeName = organisation['details']['organisationType']['translatedServiceName']
                subTypeInfo = None
        # print(typeName)
        # print(subTypeName)
            
        # contact name, contact title, contact email, contact phone
        contactName, contactTitle, contactEmail, contactPhone = '', '', '', ''
#        persons = list()
        if not organisation['people'] == None:
            contactName = ';'.join(['{0} {1}'.format(xstr(person['firstname']), xstr(person['name'])) for person in organisation['people']])
            contactTitle = ';'.join(['{0}'.format(xstr(person['title'])) for person in organisation['people']])
            contactEmail = ';'.join(['{0}'.format(xstr(person['mail'])) for person in organisation['people']])
            contactPhone = ';'.join(['{0} {1}'.format(xstr(person['phone']), xstr(person['mobile'])) for person in organisation['people']])

            #for person in organisation['people']:
            #    persons.append('{0} {1}; '.format(person['firstname'], person['name']))
        #people = concatenate_listitems(persons)
        
        # infrastructures
        infrastructures = organisation['infrastructures']
       
        # places
        places = organisation['places']
        
        # organisationActivities
        # organisationActivityAudience
        organisationActivities = list()
        organisationActivityAudiences = list()
        if not organisation['organizationActivities'] == None:
            for organisationActivity in organisation['organizationActivities']:
                organisationActivities.append(organisationActivity['activityId'])
                for organisationActivityAudience in organisationActivity['organisationActivityAudience']:
                    organisationActivityAudiences.append(organisationActivityAudience['audienceId'])
             
        organisations.append(
            [organisation['basicInfo']['id'],
             organisation['basicInfo']['nameEn'],
             organisation['basicInfo']['nameFr'],
             organisation['basicInfo']['nameNl'],
             organisation['details']['status'],
             organisation['details']['descriptionEn'],
             organisation['details']['descriptionFr'],
             organisation['details']['descriptionNl'],             
             organisation['details']['infraManager'],
             organisation['details']['isClub'], 
             typeName, # type name
             subTypeName, # subtype name
             subTypeInfo, # subtype info
             organisation['basicInfo']['referenceKey'],
             organisation['details']['companyNumber'],
             organisation['details']['vat'],
             organisation['details']['legalName'],
             status_dict[organisation['details']['legalStatus']],
             contactName, # contact name
             contactTitle, # contact title
             contactEmail, # contact email
             contactPhone, # contact phone
             infrastructures,
             places,
             organisationActivities,
             organisationActivityAudiences
             ])
        
    # Convert to pandas dataframe
    df_organisations = pd.DataFrame(organisations[1:], columns=organisations[0])
    return df_organisations


def getPlaces(end_point, headers, request_body):
    """
    Parameters
    ----------
    end_point : string
        API URL endpoint
    headers : dictionary
        headers, connection details
    request_body : dictionary
        data to pass to the API request to filter the data

    Returns
    -------
    events - Nested list
    """
    url = end_point + '/api/Place/GetPlaces'
    
    # Launch API Call
    response = requests.post(url, headers=headers, data=json.dumps(request_body))
        
    # Format response into a list
    places_extended_list = response.json()['response']
    # print(places_extended_list)
    places = []
    # append header names
    places.append(['id', 'nameEn', 'nameFr', 'nameNl', 'status', 
                   'streetFr', 'streetNl', 'number', 'postCode', 'city',
                   'address', 'isUrbisAddress', 'urbisRef_x', 'urbisRef_y', 'sector',
                   'ownerType','isPublic', 'isSchool',
                   'property_carparking_isAvailable', 'property_carSpace',
                   'property_carSpacePMR', 'property_carSpaceVIP', 'property_carSpaceBus',
                   'property_hasConvivialityArea', 'property_bikeparking_isAvailable',
                   'property_bikeparking_totalSpaces', 'property_bikeparking_isSecured',
                   'property_bikeparking_isFullyCovered', 'property_playground',
                   'infrastructures', 'organisations'])
    for i, place in enumerate(places_extended_list):
        if not place['basicInfo'] == None:
            coord_x = None
            coord_y = None
            if place['details']['addresses'][0]['urbisRef'] != None:
                coords = place['details']['addresses'][0]['urbisRef']
                #print(coords)
                coord_x = float(coords.split(',')[1][:-1])
                coord_y = float(coords.split(',')[0][1:])
            
            property_carparking_isAvailable = None    
            property_carSpace = None
            property_carSpacePMR = None
            property_carSpaceVIP = None
            property_carSpaceBus = None
            property_hasConvivialityArea = None
            property_bikeparking_isAvailable = None
            property_bikeparking_totalSpaces = None
            property_bikeparking_isSecured = None
            property_bikeparking_isFullyCovered  = None
            property_playground = None
    
            if not place['properties'] == None:
                for prop in place['properties']:
                    # print('label is: {0}'.format(prop['type']['translatedLabel']))
        
                    # properties car parking, cafetaria, bike parking, playground
                    if prop['type']['translatedLabel'] == 'Parking':
                        property_carparking_isAvailable = prop['boolean']
                    
                    if prop['type']['translatedLabel'] == 'Car space':
                        property_carSpace = prop['text']
        
                    if prop['type']['translatedLabel'] == 'Car Space-PMR':
                        property_carSpacePMR = prop['text']
        
                    if prop['type']['translatedLabel'] == 'Car Space-VIP':
                        property_carSpaceVIP = prop['text']
        
                    if prop['type']['translatedLabel'] == 'Car Space-Bus':
                        property_carSpaceBus = prop['text']
        
        
                    if prop['type']['translatedLabel'] == 'Conviviality Area':
                        property_hasConvivialityArea = prop['boolean']
        
        
                    if prop['type']['translatedLabel'] == 'Bike parking':
                        property_bikeparking_isAvailable = prop['boolean']
                        
                    if prop['type']['translatedLabel'] == 'Total number of spaces':
                        property_bikeparking_totalSpaces = prop['text']
        
                    if prop['type']['translatedLabel'] == 'Secured':
                        property_bikeparking_isSecured = prop['boolean']
        
                    if prop['type']['translatedLabel'] == 'Fully covered':
                        property_bikeparking_isFullyCovered = prop['boolean']
        
        
                    if prop['type']['translatedLabel'] == 'Playground':
                        property_playground = prop['boolean']
                        
                    #if prop['type']['translatedLabel'] == 'Min':
                    #    property_playgroundMinAge = prop['text']                   
                    #if prop['type']['translatedLabel'] == 'Max':
                    #    property_playgroundMaxAge = prop['text']   
                        
                    #if prop['type']['translatedLabel'] == 'Other':
                    #    property_isOther = prop['boolean']        
            
            # print(places)
            places.append(
                [place['basicInfo']['id'],
                 place['basicInfo']['nameEn'],
                 place['basicInfo']['nameFr'],
                 place['basicInfo']['nameNl'],
                 place['details']['status'],
                 place['details']['addresses'][0]['streetFR'],
                 place['details']['addresses'][0]['streetNL'],
                 place['details']['addresses'][0]['number'],
                 place['details']['addresses'][0]['postCode'],
                 place['details']['addresses'][0]['city'],
                 '{0} {1} {2} {3}'.format(place['details']['addresses'][0]['streetFR']
                                          , place['details']['addresses'][0]['number']
                                          , place['details']['addresses'][0]['postCode']
                                          , place['details']['addresses'][0]['city']),
                 place['details']['addresses'][0]['isUrbisAddress'],
                 coord_x,
                 coord_y,
                 place['details']['sector'],
                 place['details']['ownerType'],  
                 place['details']['public'],
                 place['details']['isSchool'], 
                 property_carparking_isAvailable,
                 property_carSpace,
                 property_carSpacePMR,
                 property_carSpaceVIP, 
                 property_carSpaceBus, 
                 property_hasConvivialityArea,
                 property_bikeparking_isAvailable,
                 property_bikeparking_totalSpaces,
                 property_bikeparking_isSecured, 
                 property_bikeparking_isFullyCovered,
                 property_playground,
                 place['infrastructures'],
                 place['organisations']
                 ])
        
    # Convert to pandas dataframe
    df_places = pd.DataFrame(places[1:], columns=places[0])

    return df_places

def getSubsidies(end_point, headers, request_body):
    """
    Parameters
    ----------
    end_point : string
        API URL endpoint
    headers : dictionary
        headers, connection details
    request_body : dictionary
        data to pass to the API request to filter the data

    Returns
    -------
    events - Nested list
    """
    url = end_point + '/api/Subsidy/GetSubsidies'
    
    # Subsidy status dictionary
    # status_dict = {'N':'N-code: Draft?', 'V':'Validated', 'E':'Exported', 'L':'Legacy', 'D':'Draft', 'R':'Refused', 'W':'Waiting for validation'}
    
    # Launch API Call
    response = requests.post(url, headers=headers, data=json.dumps(request_body))
        
    # Format response into a list
    subsidies_extended_list = response.json()['response']
    subsidies = []
    
    # append header names
    subsidies.append(['id', 'name', 'subsidy organisation', 'more information', 'status', 'date', 'amount',
                      'modification date',
                      'operating subsidy', 'subsidy type', 'starting date', 'closing date',
                      'contact', 
                      'organisationMainId',
                      'organisationSubsidyBpl',
                      'infrastructureId'
                      ])
    for i, subsidy in enumerate(subsidies_extended_list):

        subsidies.append(
            [subsidy['id'],
             subsidy['type']['name'],  
             subsidy['subsidisingPartner']['name'], # subsidy organisation
             subsidy['type']['informationPage'], # more information
             subsidy['status'], # status_dict[subsidy['status']],
             stringToDate(subsidy['creationDate']),
             subsidy['amount'],
             
             stringToDate(subsidy['modificationDate']), # modification date
             
             subsidy['type']['operatingSubsidy'], # operating subsidy
             subsidy['type']['typeOfSubsidy'], # subsidy type
             stringToDate(subsidy['type']['startDate']), # starting date
             stringToDate(subsidy['type']['endDate']), # closing date
             subsidy['contact'],
             subsidy['organisationMainId'],
             subsidy['organisationSubsidyBpl'],
             subsidy['infrastructureId']
             ])
        
    # Convert to pandas dataframe
    df_subsidies = pd.DataFrame(subsidies[1:], columns=subsidies[0])
    return df_subsidies

def stringToDate(inputString):
    """
    Converts string to date values and format date to dd/mm/yyyy format
    
    Returns
    -------
    date : date
        formatted date (dd-mm-yyyy).

    """
    # Convert string to dates if not null
    if inputString is None or inputString == '':
        date = inputString
    else:
        try:
            # Date without nanoseconds
            date = datetime.strptime(inputString, '%Y-%m-%dT%H:%M:%S').date()
        except:
            # date with nanoseconds
            date = datetime.strptime(inputString, '%Y-%m-%dT%H:%M:%S.%f').date()
    return date


def stringToTime(inputString):
    """
    Converts string to datetime values and format date to dd/mm/yyyy format
    
    Returns
    -------
    time : datetime
        formatted date (dd-mm-yyyy).

    """
    # Convert string to times if not null
    if inputString is None or inputString == '':
        time = inputString
    else:
        try:
            # Time without nanoseconds
            time = datetime.strptime(inputString, '%Y-%m-%dT%H:%M:%S').time()
        except:
            # time with nanoseconds
            time = datetime.strptime(inputString, '%Y-%m-%dT%H:%M:%S.%f').time()
    return time


def getFacilities(end_point, headers, request_body):
    """
    Parameters
    ----------
    end_point : string
        API URL endpoint
    headers : dictionary
        headers, connection details
    request_body : dictionary
        data to pass to the API request to filter the data

    Returns
    -------
    events - Nested list
    """
    url = end_point + '/api/Facility/GetFacilities'
    
    # Launch API Call
    response = requests.post(url, headers=headers, data=json.dumps(request_body))
        
    # Format response into a list
    if response.status_code == 200:
        facilities_extended_list = response.json()['response']
    else:
        facilities_extended_list = []
    facilities = []
    
    # append header names
    facilities.append(['id', 'mainId', 'facilityTypeId', 'nameEn', 'nameFr', 'nameNl', 
                       #'facilityTypeName',
                       'accessiblePRM', 'infrastructureMainId', 'organisationMainId', 'status',
                       'activities', 
                       'facilityTypeValues'
                      ])
    for i, facility in enumerate(facilities_extended_list):
        facilities.append(
            [facility['basicInfo']['id'],
             facility['basicInfo']['mainId'],
             facility['basicInfo']['type']['id'],
#             facility['basicInfo']['facilityLg'][0]['name'],
             facility['basicInfo']['type']['name']['translations'][0]['translation'],
             facility['basicInfo']['type']['name']['translations'][1]['translation'],
             facility['basicInfo']['type']['name']['translations'][2]['translation'],
             facility['details']['accessiblePRM'],
             facility['details']['infrastructureMainId'],
             facility['details']['organisationMainId'],
             facility['details']['status'],
             facility['activities'],
             facility['facilityTypeValues']
             ])
        
    # Convert to pandas dataframe
    df_facilities = pd.DataFrame(facilities[1:], columns=facilities[0])

    return df_facilities




def concatenate_listitems(list):
    separator = ';'
    return separator.join(list)

def concatenate_listitems_key(list, value):
    separator = ";"
    return [separator.join(listitem.get(value)) for i, listitem in enumerate(list)]


def formatAddressType(lst_addresses, lang='fr', address_type='localisation'):
    """
    Parameters
    ----------
    lst_addresses : list with dictionnaries
        Addressess
    lang : string, optional
        Language: 'fr', 'nl' or 'en'. The default is 'fr'.
    type : string, optional
        Type of address: 'localisation', 'postale', 'livraison'. The default is 'localisation'.

    Returns
    -------
    string: formatted address.
    """
    # Set default value to return 
    address = None
    # If at least one address available in the list
    if len(lst_addresses) > 0:
        # Loop over the possible addresses and pick the correct type of address
        for i, dict_address in enumerate(lst_addresses):
            # Return type address
            if str.lower(dict_address.get('type')) == str.lower(address_type):
                # select language
                if str.lower(lang) == 'fr':
                    street = dict_address.get('streetFR')
                elif str.lower(lang) == 'nl':
                    street = dict_address.get('streetNL')
                elif str.lower(lang) == 'en':
                    street = dict_address.get('streetEN')
                address = '{0} {1} {2} {3}'.format(street, dict_address.get('number'), dict_address.get('postCode'), dict_address.get('city'))
    return address

def formatAddress(lst_addresses, lang='fr'):
    """
    Parameters
    ----------
    lst_addresses : list with dictionnaries
        Addressess
    lang : string, optional
        Language: 'fr', 'nl' or 'en'. The default is 'fr'.

    Returns
    -------
    string: formatted address.
    """
    # Set default value to return 
    address = None
    # If at least one address available in the list
    if len(lst_addresses) > 0:
        # Loop over the possible addresses and pick the correct type of address
        for i, dict_address in enumerate(lst_addresses):
            # select language
            if str.lower(lang) == 'fr':
                street = dict_address.get('streetFR')
            elif str.lower(lang) == 'nl':
                street = dict_address.get('streetNL')
            elif str.lower(lang) == 'en':
                street = dict_address.get('streetEN')
            address = '{0} {1} {2} {3}'.format(street, dict_address.get('number'), dict_address.get('postCode'), dict_address.get('city'))
    return address

def xstr(s):
    if s is None:
        return ''
    else:
        return str(s)