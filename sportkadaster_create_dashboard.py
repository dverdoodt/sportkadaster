# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 10:54:48 2020

@author: dverdoodt
@description: Laucnh the creation of a report, based on the API provided by the sportkadaster.
https://api-web-sportbrussels.dev.voxteneo.com/swagger/index.html
All functions

-	Dev : https://api-web-sportbrussels.dev.voxteneo.com/swagger/index.html
-	Staging : http://staging.manager.sport.brussels/api/swagger/index.html
-	Prod : http://manager.sport.brussels/api/swagger/index.html

Read all data from API
Write all data to postgresql DB
Create materialized views in DB
Write the results of these queries to Excel-files / maps / HTML-reports (cartopy)

"""
# =========================================
# Import modules
# =========================================
import pandas as pd
import sportkadaster_api_tools as api_tools
from datetime import datetime
from configparser import ConfigParser
import sqlalchemy
from sqlalchemy import create_engine

# =========================================
# Read config-file
# =========================================
config_object = ConfigParser()
config_object.read(r'C:/Users/dverdoodt/Documents/sportkadaster/config.ini')

config_parameters_api = config_object["staging"]  ## development | staging | production
config_parameters_db = config_object["postgresql"]  ## development | staging | production

# Read connection info from config file
END_POINT = config_parameters_api["END_POINT"]
API_KEY = config_parameters_api["API_KEY"]

# Read connection info from config file
host = config_parameters_db["host"]
user = config_parameters_db["user"]
password = config_parameters_db["password"]
db = config_parameters_db["db"]
port = config_parameters_db["port"]
schema = config_parameters_db["schema"]

# =========================================
# Set parameters
# excel writer output file
# =========================================
## Define Excel output file
output_file = './output/dashboard_sportkadaster_{0}.xlsx'.format(datetime.now().strftime("%Y%m%d"))
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
# Activity
# De verschillende sport activiteiten die zijn geregistreerd in het sportkadaster.
# Als je "0" ingeeft voor "page" of "id" wordt er niet gefilterd, en worden alle resultaten weergegeven.
# Als "name" bij activity filter een lege string komt overeen met de null-waarde.
# =========================================

## Launch API request
## request_body = api_tools.makeRequestBodyActivity()
## df_activities = api_tools.getActivities(END_POINT, headers, request_body)
## df_mainActivities = api_tools.getMainActivities(END_POINT, headers, request_body)

request_body_fr = api_tools.makeRequestBodyActivity(language='fr')
request_body_nl = api_tools.makeRequestBodyActivity(language='nl')
request_body_en = api_tools.makeRequestBodyActivity(language='en')

df_activities_fr = api_tools.getActivities(END_POINT, headers, request_body_fr)
df_activities_nl = api_tools.getActivities(END_POINT, headers, request_body_nl)
df_activities_en = api_tools.getActivities(END_POINT, headers, request_body_en)

# merge information to combine three languages
df_activities = pd.DataFrame(
        data= {'id': df_activities_fr['id'],
               'parentId': df_activities_fr['parentId'],
               'nameFr': df_activities_fr['translatedName'],
               'nameNl': df_activities_nl['translatedName'],
               'nameEn': df_activities_en['translatedName']})

# =========================================
# Audience
# Doelpublieken
# =========================================
## Launch API request
## request_body = api_tools.makeRequestBodyAudience()
## df_audiences = api_tools.getAudiences(END_POINT, headers, request_body)

request_body_fr = api_tools.makeRequestBodyAudience(language='fr')
request_body_nl = api_tools.makeRequestBodyAudience(language='nl')
request_body_en = api_tools.makeRequestBodyAudience(language='en')
df_audiences_fr = api_tools.getAudiences(END_POINT, headers, request_body_fr)
df_audiences_nl = api_tools.getAudiences(END_POINT, headers, request_body_nl)
df_audiences_en = api_tools.getAudiences(END_POINT, headers, request_body_en)

df_audiences = pd.DataFrame(
        data={'id': df_audiences_fr['id'],
              'name': df_audiences_fr['name'],
              'nameFr': df_audiences_fr['translatedName'],
              'nameNl': df_audiences_nl['translatedName'],
              'nameEn': df_audiences_en['translatedName'],
              'minAge': df_audiences_fr['minAge'],
              'maxAge': df_audiences_fr['maxAge'],
              'disabled': df_audiences_fr['disabled'],
              'gender': df_audiences_fr['gender'],
              'type': df_audiences_fr['type']})

# =========================================
# Event
# =========================================
## Launch API request
request_body = api_tools.makeRequestBodyEvents(isRegular=True, language='fr')
df_events_regular = api_tools.getEvents(END_POINT, headers, request_body)

request_body = api_tools.makeRequestBodyEvents(isRegular=False, language='fr')
df_events_irregular = api_tools.getEvents(END_POINT, headers, request_body)

## Concatenate both event types into one dataframe
df_events = pd.concat([df_events_regular, df_events_irregular], ignore_index=True)

# =========================================
# Facility: GetFacilityType
# =========================================
## Launch API request
## request_body = api_tools.makeRequestBodyFacilityType()
## df_facilityTypes = api_tools.getFacilityTypes(END_POINT, headers, request_body)

request_body_fr = api_tools.makeRequestBodyFacilityType(language='fr')
request_body_nl = api_tools.makeRequestBodyFacilityType(language='nl')
request_body_en = api_tools.makeRequestBodyFacilityType(language='en')
df_facilityTypes_fr = api_tools.getFacilityTypes(END_POINT, headers, request_body_fr)
df_facilityTypes_nl = api_tools.getFacilityTypes(END_POINT, headers, request_body_nl)
df_facilityTypes_en = api_tools.getFacilityTypes(END_POINT, headers, request_body_en)

df_facilityTypes = pd.DataFrame(
        data={'id': df_facilityTypes_fr['id'],
              'nameFr': df_facilityTypes_fr['translatedName'],
              'nameNl': df_facilityTypes_nl['translatedName'],
              'nameEn': df_facilityTypes_en['translatedName'],
              'status': df_facilityTypes_fr['status'],
              'facilityTypesFr': df_facilityTypes_fr['facilityTypes'],
              'facilityTypesNl': df_facilityTypes_nl['facilityTypes'],
              'facilityTypesEn': df_facilityTypes_en['facilityTypes']
              })


# =========================================
# Infrastructure
# =========================================
## Launch API Request
## request_body = api_tools.makeRequestBodyInfrastructure(language='nl', infrastructureId='75b53bce-aaa0-4599-afff-a5ca227cc4de')
## df_infrastructures = api_tools.getInfrastructures(END_POINT, headers, request_body)

request_body_fr = api_tools.makeRequestBodyInfrastructure(language='fr')
request_body_nl = api_tools.makeRequestBodyInfrastructure(language='nl')
request_body_en = api_tools.makeRequestBodyInfrastructure(language='en')
df_infrastructures_fr = api_tools.getInfrastructures(END_POINT, headers, request_body_fr)
df_infrastructures_nl = api_tools.getInfrastructures(END_POINT, headers, request_body_nl)
df_infrastructures_en = api_tools.getInfrastructures(END_POINT, headers, request_body_en)

df_infrastructures = pd.DataFrame(
        data={'id': df_infrastructures_fr['id'],
              'mainId': df_infrastructures_fr['mainId'],
              'referenceKey': df_infrastructures_fr['referenceKey'],
              'nameFr': df_infrastructures_fr['name'],
              'nameNl': df_infrastructures_nl['name'],
              'nameEn': df_infrastructures_en['name'],
              'organisations': df_infrastructures_fr['organisations'],
              'clubs': df_infrastructures_fr['clubs'],
              'facilities': df_infrastructures_fr['facilities'],
              'status': df_infrastructures_en['status'],
              'details_automatedExternalDefibrillator': df_infrastructures_fr['details_automatedExternalDefibrillator'],
              'details_energyFile': df_infrastructures_fr['details_energyFile'],
              'details_inPlaceId': df_infrastructures_fr['details_inPlaceId'],
              'infrastructureProperties': df_infrastructures_en['infrastructureProperties']
             })


# =========================================
# Organisation
# Hoe kunnen de datums gebruikt worden om de organisaties te filteren?
# Clubs and no-clubs
# =========================================
# Launch API Request
request_body = api_tools.makeRequestBodyOrganisation()
df_organisations_isClub = api_tools.getOrganisations(END_POINT, headers, request_body)

request_body = api_tools.makeRequestBodyOrganisation(isClub=False)
df_organisations_isNotClub = api_tools.getOrganisations(END_POINT, headers, request_body)

## Concatenate both event types into one dataframe
df_organisations = pd.concat([df_organisations_isClub, df_organisations_isNotClub], ignore_index=True)


# =========================================
# Place
# sample: id=0a3c4f9c-651d-458e-83c7-b0899b2c69bb
# =========================================
# Launch API Request
request_body = api_tools.makeRequestBodyPlaces()
df_places = api_tools.getPlaces(END_POINT, headers, request_body)

#gdf_places = gpd.GeoDataFrame(
#    df_places, geometry = gpd.points_from_xy(df_places.urbisRef_y, df_places.urbisRef_x))

# =========================================
# Subsidy
# =========================================
# Launch API Request
request_body = api_tools.makeRequestbodySubsidy()
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
request_body = api_tools.makeRequestBodyFacility()
df_facilities = api_tools.getFacilities(END_POINT, headers, request_body)


# =========================================
# Write to Excel file
# =========================================
#with pd.ExcelWriter(output_file) as writer:  
#    # Activity
#    df_activities.to_excel(writer, sheet_name='activities', index=False, freeze_panes=(1,0))
#    ## df_mainActivities.to_excel(writer, sheet_name='mainactivities', index=False, freeze_panes=(1,0))
#    
#    # Audience
#    df_audiences.to_excel(writer, sheet_name='audiences', index=False, freeze_panes=(1,0))
#    
#    # Event
#    #df_events_regular.to_excel(writer, sheet_name='events_regular', index=False, freeze_panes=(1,0))
#    #df_events_irregular.to_excel(writer, sheet_name='events_irregular', index=False, freeze_panes=(1,0))
#    df_events.to_excel(writer, sheet_name='events', index=False, freeze_panes=(1,0))
#    
#    # Facility
#    df_facilityTypes.to_excel(writer, sheet_name='facilityTypes', index=False, freeze_panes=(1,0))
#    df_facilities.to_excel(writer, sheet_name='facilities', index=False, freeze_panes=(1,0))
#    
#    # Infrastructure
#    df_infrastructures.to_excel(writer, sheet_name='infrastructures', index=False, freeze_panes=(1,0))
#    
#    
#    # Organisation
#    df_organisations.to_excel(writer, sheet_name='organisations', index=False, freeze_panes=(1,0))
#    
#    # Place
#    df_places.to_excel(writer, sheet_name='places', index=False, freeze_panes=(1,0))
#    
#    # Subsidy
#    df_subsidies.to_excel(writer, sheet_name='subsidies', index=False, freeze_panes=(1,0))
    
# =========================================
# Write to PostgreSQL DB
# =========================================
## Connect to the database and set up a cursor object which is used to issue commands.
# Database info
## 'postgres' or 'postgresql+psycopg2'
db_url = '{0}://{1}:{2}@{3}:{4}/{5}?gssencmode=disable'.format('postgres', user, password, host, port, db)
engine = create_engine(db_url)
print(engine)

## Test the DB connection
with engine.connect() as connection:
    result = connection.execute("SELECT usename FROM pg_user;")
    for row in result:
        print("username:", row['usename'])

## Write dataframe to non-spatial table: to_sql()
## Write geodataframe to spatial table: to_postgis()
try:
    ## gdf.to_postgis(name="test", con=engine, schema='sportkadaster', if_exists='fail')
    
    # Activity
    df_activities.to_sql(name= "activity", con=engine, schema='sportkadaster', if_exists='fail')

    # Audience
    df_audiences.to_sql(name= "audience", con=engine, schema='sportkadaster', if_exists='fail')
    
    # Event
    ##df_events_regular.to_sql(name= "event_regular", con=engine, schema='sportkadaster', if_exists='fail')
    ##df_events_irregular.to_sql(name= "event_irregular", con=engine, schema='sportkadaster', if_exists='fail')
    df_events.to_sql(name= "event", con=engine, schema='sportkadaster', if_exists='fail', 
                     dtype={"eventActivities": sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.INTEGER),
                            "eventAudiences": sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.INTEGER),
                            "eventLanguages": sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.TEXT)})

    # Facility
    df_facilityTypes.to_sql(name= "facility_type", con=engine, schema='sportkadaster', if_exists='fail',
                            dtype={"facilityTypesFr": sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.TEXT),
                                   "facilityTypesNl": sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.TEXT),
                                   "facilityTypesEn": sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.TEXT)})
    df_facilities.to_sql(name= "facility", con=engine, schema='sportkadaster', if_exists='fail',
                         dtype={"activities":sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.INTEGER),
                                "facilityTypeValues":sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.INTEGER)})
    
    # Infrastructure
    df_infrastructures.to_sql(name= "infrastructure", con=engine, schema='sportkadaster', if_exists='fail',
                    dtype={'organisations': sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.TEXT),
                           'clubs': sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.TEXT),
                           'facilities': sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.TEXT)
                            })

    
    # Organisation
    df_organisations.to_sql(name= "organisation", con=engine, schema='sportkadaster', if_exists='fail',
                    dtype={'infrastructures': sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.TEXT),
                           'places': sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.TEXT),
                           'organisationActivities': sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.INTEGER),
                           'organisationActivitiesAudiences': sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.INTEGER)})
    
    # Place
    df_places.to_sql(name= "place", con=engine, schema='sportkadaster', if_exists='fail',
                     dtype={
                             #'urbisRef': sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.TEXT),
                            'infrastructures': sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.TEXT),
                            'organisations': sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.TEXT) 
                             })
    
#    gdf_places.to_postgis(name="place", con=engine, schema='sportkadaster', if_exists='fail',
#                      dtype={
#                             #'urbisRef': sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.TEXT),
#                            'infrastructures': sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.TEXT),
#                            'organisations': sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.types.TEXT) 
#                             })

    
    # Subsidy
    df_subsidies.to_sql(name= "subsidy", con=engine, schema='sportkadaster', if_exists='fail', 
                        dtype={"operating subsidy": sqlalchemy.types.JSON,
                               "subsidy type": sqlalchemy.types.JSON,
                               "organisationSubsidyBpl": sqlalchemy.types.JSON})
  
except ValueError as vx:
    print(vx)
except Exception as ex:  
    print(ex)
else:
    print("PostgreSQL Tables have been created successfully.");

## Add Primary key (and eventually FK) constraints to the tables.

# =========================================
# Connect to PostgreSQL
# Add Primary Keys
# Refresh materialized views
# =========================================
with engine.connect() as connection:
    result = connection.execute('ALTER TABLE sportkadaster.activity ADD CONSTRAINT activity_pk PRIMARY KEY ("index");')
    result = connection.execute('ALTER TABLE sportkadaster.audience ADD CONSTRAINT audience_pk PRIMARY KEY ("index");')
    result = connection.execute('ALTER TABLE sportkadaster."event" ADD CONSTRAINT event_pk PRIMARY KEY ("index");')
    result = connection.execute('ALTER TABLE sportkadaster.facility ADD CONSTRAINT facility_pk PRIMARY KEY ("index");')
    result = connection.execute('ALTER TABLE sportkadaster.facility_type ADD CONSTRAINT facility_type_pk PRIMARY KEY ("index");')
    result = connection.execute('ALTER TABLE sportkadaster.infrastructure ADD CONSTRAINT infrastructure_pk PRIMARY KEY ("index");')
    result = connection.execute('ALTER TABLE sportkadaster.organisation ADD CONSTRAINT organisation_pk PRIMARY KEY ("index");')
    result = connection.execute('ALTER TABLE sportkadaster.place ADD CONSTRAINT place_pk PRIMARY KEY ("index");')
    result = connection.execute('ALTER TABLE sportkadaster.subsidy ADD CONSTRAINT subsidy_pk PRIMARY KEY ("index");')
    print('Added primary keys')

#
#with engine.connect() as connection:
#    result = connection.execute('refresh materialized view sportkadaster.activity_mvw;')
#    result = connection.execute('refresh materialized view sportkadaster.audience_mvw;')
#    result = connection.execute('refresh materialized view sportkadaster.event_mvw;')
#    result = connection.execute('refresh materialized view sportkadaster.facility_mvw;')
#    result = connection.execute('refresh materialized view sportkadaster.facility_type_mvw;')
#    result = connection.execute('refresh materialized view sportkadaster.infrastructure_mvw;')
#    result = connection.execute('refresh materialized view sportkadaster.organisation_mvw;')
#    result = connection.execute('refresh materialized view sportkadaster.place_missing_geom_mvw;')
#    result = connection.execute('refresh materialized view sportkadaster.place_mvw;')
#    result = connection.execute('refresh materialized view sportkadaster.subsidy_mvw;')
#    result = connection.execute('refresh materialized view sportkadaster.subsidy_grantee_mvw;')
#    result = connection.execute('refresh materialized view sportkadaster.subsidy_grantor_mvw;')
#    print('Refreshed materialized views')
    
# =========================================
# Read from PostgreSQL DB and write to Excel
# =========================================
df_activity_mvw = pd.read_sql_table(table_name='activity_mvw', con=engine, schema='sportkadaster', index_col=None)
df_audience_mvw = pd.read_sql_table(table_name='audience_mvw', con=engine, schema='sportkadaster', index_col=None)
df_event_mvw = pd.read_sql_table(table_name='event_mvw', con=engine, schema='sportkadaster', index_col=None)
df_facility_mvw = pd.read_sql_table(table_name='facility_mvw', con=engine, schema='sportkadaster', index_col=None)
df_facility_type_mvw = pd.read_sql_table(table_name='facility_type_mvw', con=engine, schema='sportkadaster', index_col=None)
df_infrastructure_mvw = pd.read_sql_table(table_name='infrastructure_mvw', con=engine, schema='sportkadaster', index_col=None)
df_organisation_mvw = pd.read_sql_table(table_name='organisation_mvw', con=engine, schema='sportkadaster', index_col=None)
df_place_missing_geom_mvw = pd.read_sql_table(table_name='place_missing_geom_mvw', con=engine, schema='sportkadaster', index_col=None)
df_place_mvw = pd.read_sql_table(table_name='place_mvw', con=engine, schema='sportkadaster', index_col=None)
df_subsidy_mvw = pd.read_sql_table(table_name='subsidy_mvw', con=engine, schema='sportkadaster', index_col=None)
df_subsidy_grantee_mvw = pd.read_sql_table(table_name='subsidy_grantee_mvw', con=engine, schema='sportkadaster', index_col=None)
df_subsidy_grantor_mvw = pd.read_sql_table(table_name='subsidy_grantor_mvw', con=engine, schema='sportkadaster', index_col=None)


with pd.ExcelWriter(output_file) as writer:  
    # Activity
    df_activity_mvw.to_excel(writer, sheet_name='activity_mvw', index=False, freeze_panes=(1,0))
    
    # Audience
    df_audience_mvw.to_excel(writer, sheet_name='audience_mvw', index=False, freeze_panes=(1,0))
    
    # Event
    df_event_mvw.to_excel(writer, sheet_name='event_mvw', index=False, freeze_panes=(1,0))
    
    # Facility
    df_facility_mvw.to_excel(writer, sheet_name='facility_mvw', index=False, freeze_panes=(1,0))
    df_facility_type_mvw.to_excel(writer, sheet_name='facility_type_mvw', index=False, freeze_panes=(1,0))
    
    # Infrastructure
    df_infrastructure_mvw.to_excel(writer, sheet_name='infrastructure_mvw', index=False, freeze_panes=(1,0))
    
    # Organisation
    df_organisation_mvw.to_excel(writer, sheet_name='organisation_mvw', index=False, freeze_panes=(1,0))
    
    # Place
    df_place_missing_geom_mvw.to_excel(writer, sheet_name='place_missing_geom_mvw', index=False, freeze_panes=(1,0))
    df_place_mvw.to_excel(writer, sheet_name='place_mvw', index=False, freeze_panes=(1,0))
    
    # Subsidy
    df_subsidy_mvw.to_excel(writer, sheet_name='subsidy_mvw', index=False, freeze_panes=(1,0))
    df_subsidy_grantee_mvw.to_excel(writer, sheet_name='subsidy_grantee_mvw', index=False, freeze_panes=(1,0))
    df_subsidy_grantor_mvw.to_excel(writer, sheet_name='subsidy_grantor_mvw', index=False, freeze_panes=(1,0))
