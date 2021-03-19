/*
 * Create PK's
 * 
 */
ALTER TABLE sportkadaster.activity ADD CONSTRAINT activity_pk PRIMARY KEY ("index");
ALTER TABLE sportkadaster.audience ADD CONSTRAINT audience_pk PRIMARY KEY ("index");
ALTER TABLE sportkadaster."event" ADD CONSTRAINT event_pk PRIMARY KEY ("index");
ALTER TABLE sportkadaster.facility ADD CONSTRAINT facility_pk PRIMARY KEY ("index");
ALTER TABLE sportkadaster.facility_type ADD CONSTRAINT facility_type_pk PRIMARY KEY ("index");
ALTER TABLE sportkadaster.infrastructure ADD CONSTRAINT infrastructure_pk PRIMARY KEY ("index");
ALTER TABLE sportkadaster.organisation ADD CONSTRAINT organisation_pk PRIMARY KEY ("index");
ALTER TABLE sportkadaster.place ADD CONSTRAINT place_pk PRIMARY KEY ("index");
ALTER TABLE sportkadaster.subsidy ADD CONSTRAINT subsidy_pk PRIMARY KEY ("index");

/*
 * Refresh Materialized views
 * 
 */
refresh materialized view activity_mvw;
refresh materialized view audience_mvw;
refresh materialized view event_mvw;
refresh materialized view facility_mvw;
refresh materialized view facility_type_mvw;
refresh materialized view infrastructure_mvw;
refresh materialized view organisation_mvw;
refresh materialized view place_mvw;
refresh materialized view subsidy_mvw;
refresh materialized view subsidy_grantee_mvw;
refresh materialized view subsidy_grantor_mvw;

/*
 * Drop Materialized views
 * 
 */
drop materialized view activity_mvw;
drop materialized view audience_mvw;
drop materialized view event_mvw;
drop materialized view facility_mvw;
drop materialized view facility_type_mvw;
drop materialized view infrastructure_mvw;
drop materialized view organisation_mvw;
drop materialized view place_mvw;
drop materialized view subsidy_mvw;
drop materialized view subsidy_grantee_mvw;
drop materialized view subsidy_grantor_mvw;


/*
 * Drop tables
 * 
 */
drop table activity;
drop table audience;
drop table "event";
drop table facility;
drop table facility_type;
drop table infrastructure;
drop table organisation;
drop table place;
drop table subsidy;


/*
 * Views for sportkadaster
 * 
 */

-- drop materialized view place_missing_geom_vw;
create materialized view place_missing_geom_mvw as 
select *
from place
where "urbisRef_x" is null or "urbisRef_y" is null;
grant select on table sportkadaster.place_missing_geom_mvw to perspective;

--------------------------------------
-- Activity
--------------------------------------
-- drop materialized view activity_mvw;
create materialized view activity_mvw as
select 
	a.id,
	a."parentId",
	a."nameFr",
	a."nameNl",
	a."nameEn"
from activity a;
GRANT SELECT ON TABLE sportkadaster.activity_mvw TO perspective;


--------------------------------------
-- Audience
--------------------------------------
-- drop materialized view audience_mvw;
create materialized view audience_mvw as 
select
	a.id, 
	a."nameFr",
	a."nameNl",
	a."nameEn",
	a."minAge",
	a."maxAge",
	a.disabled,
	a.gender,
	a."type"
from audience a;
GRANT SELECT ON TABLE sportkadaster.audience_mvw TO perspective;


--------------------------------------
-- Event
--------------------------------------
-- It is easier to write e.*, but in order to place the columns in the right order, the views needs to be constructed column by column.
-- drop materialized view event_mvw;
create materialized view event_mvw as 
with act_items as (select id, "nameFr", "nameNl", "nameEn" from activity),
	 aud_items as (select id, "nameFr", "nameNl", "nameEn", "minAge", "maxAge", disabled from audience)
select distinct on (e.id)
	-- e.*,
	e.id, 
	e."isVisibleOnWebsite", 
	e."activityType", 
	CASE e.status
    WHEN 'D' THEN 'Draft'
    WHEN 'V' THEN 'Validated'
    ELSE e.status 
    END,
	e."name",
	e.description, 
	e."placeMainId", 
	p."nameNl" as placename_fr,
	p."nameNl" as placename_nl,
	p."nameNl" as placename_en,
	e.place, 
	e."isPublic", 
	e."isCompetitive", 
	e."isEntertaining", 
	e."isFree",
	e.fares, 
	e."startDate", 
	e."startTime",
	e."endDate", 
	e."endTime",
	e."isRegular", 
	e."eventActivities",
	array_to_json(array_agg(row_to_json(act_items)) over (partition by e.id, aud_items.id)) as eventActivities_detailed,
	e."eventAudiences",
	array_to_json(array_agg(row_to_json(aud_items)) over (partition by e.id, act_items.id)) as eventAudiences_detailed,	
	e."eventLanguages",
	e.organiser,
	e.surname, 
	e.firstname, 
	e.organisation,
	o."nameFr" as organisationname_fr,
	o."nameNl" as organisationname_nl,
	o."nameEn" as organisationname_en,
	e."organiserPeople",
	e.mail, 
	e.website
from "event" e 
	left join place p on e."placeMainId" = p.id
	left join organisation o on e.organisation = o.id
	left join act_items on act_items.id = any(e."eventActivities")
	left join aud_items on aud_items.id = any(e."eventAudiences");
GRANT SELECT ON TABLE sportkadaster.event_mvw TO perspective;


--------------------------------------
-- Facility
--------------------------------------
-- drop materialized view facility_mvw;
create materialized view facility_mvw as 
with act_items as (select id, "nameFr", "nameNl", "nameEn" from activity),
	 facilitytype_items as (select id, "nameFr", "nameNl", "nameEn" from facility_type)
select distinct on (f.id)
	f.id, 
	f."mainId",
	f."facilityTypeId",
	--f."name",
	f."nameFr",
	f."nameNl",
	f."nameEn",
	f."accessiblePRM" ,
	f."infrastructureMainId",
	i."nameFr" as infrastructure_name_fr,
	i."nameNl" as infrastructure_name_nl,
	i."nameEn" as infrastructure_name_en,
	f."organisationMainId",
	o."nameFr" as organisation_name_fr,
	o."nameNl" as organisation_name_nl,
	o."nameEn" as organisation_name_en,
	f.status,
	f.activities,
	array_to_json(array_agg(row_to_json(act_items)) over (partition by f.id, act_items.id)) as activities_detailed,
	f."facilityTypeValues",
	array_to_json(array_agg(row_to_json(facilitytype_items)) over (partition by f.id, facilitytype_items.id)) as facilitytypevalues_detailed	
from "facility" f
	left join organisation o on o.id = f."organisationMainId" 
	left join infrastructure i on i.id = f."infrastructureMainId" 
	left join act_items on act_items.id = any(f.activities)
	left join facilitytype_items on facilitytype_items.id = any(f."facilityTypeValues");
GRANT SELECT ON TABLE sportkadaster.facility_mvw TO perspective;


--------------------------------------
-- Facility Type
--------------------------------------
-- drop materialized view facility_type_mvw;
create materialized view facility_type_mvw as
select
	ft.id,
	ft."nameFr",
	ft."nameNl",
	ft."nameEn",
	CASE status
    WHEN 'A' THEN 'Active'
    WHEN 'X' THEN 'Deactivated'
    ELSE ft.status 
    END,
	ft."facilityTypesFr", 
	ft."facilityTypesNl",
	ft."facilityTypesEn"
from facility_type ft;
GRANT SELECT ON TABLE sportkadaster.facility_type_mvw TO perspective;


--------------------------------------
-- Infrastructure
--------------------------------------
-- drop materialized view infrastructure_mvw;
create materialized view infrastructure_mvw as 
with	org_items as (select id, "nameFr", "nameNl", "nameEn" from organisation where "isClub" is false),
		club_items as (select id, "nameFr", "nameNl", "nameEn" from organisation where "isClub" is true),
		facility_items as (select id, "nameFr", "nameNl", "nameEn" from facility)
select
distinct on (i.id)
	i.id, 
	i."mainId",
	i."referenceKey",
	i."nameFr",
	i."nameNl",
	i."nameEn",
	i.organisations,
	array_to_json(array_agg(row_to_json(org_items)) over (partition by i.id, club_items.id, facility_items.id)) as organisations_detailed,
	i.clubs,
	array_to_json(array_agg(row_to_json(club_items)) over (partition by i.id, org_items.id, facility_items.id)) as clubs_detailed,
	i.facilities,
	array_to_json(array_agg(row_to_json(facility_items)) over (partition by i.id, org_items.id, club_items.id)) as facilities_detailed,
	CASE i.status
    WHEN 'V' THEN 'Validated'
    WHEN 'T' THEN 'Trashed'
    when 'D' then 'Draft'
    ELSE i.status 
    END,
	"details_automatedExternalDefibrillator",
	"details_energyFile",
	"details_inPlaceId",
	p."nameFr"  as placename_fr,
	p."nameNl"  as placename_nl,
	p."nameEn"  as placename_en,
	p.address,
	i."infrastructureProperties",
	st_transform(ST_SetSRID(ST_MakePoint(p."urbisRef_x", p."urbisRef_y"),4326), 31370) as geom
from infrastructure i
	left join place p on i."details_inPlaceId" = p.id
	left join org_items on org_items.id = any(i.organisations)
	left join club_items on club_items.id = any(i.clubs)
	left join facility_items on facility_items.id = any(i.facilities);
GRANT SELECT ON TABLE sportkadaster.infrastructure_mvw TO perspective;


--------------------------------------
-- Organisation
--------------------------------------
-- drop materialized view organisation_mvw;
create materialized view organisation_mvw as 
with 	inf_items as (select distinct id, "nameFr", "nameNl", "nameEn" from infrastructure),
		place_items as (select distinct id, "nameFr", "nameNl", "nameEn", address from place),
		place_geoms as (select id, st_transform(ST_SetSRID(ST_MakePoint("urbisRef_x", "urbisRef_y"),4326), 31370) as geom from place),
		act_items as (select distinct id, "nameFr", "nameNl", "nameEn" from activity),
		aud_items as (select distinct id, "nameFr", "nameNl", "nameEn", "minAge", "maxAge", disabled from audience)
select distinct on (o.id)
  	o.id,
  	o."nameFr",
  	o."nameEn",
  	o."nameNl",
	CASE o.status
    WHEN 'V' THEN 'Validated'
    WHEN 'T' THEN 'Trashed'
    when 'D' then 'Draft'
    ELSE o.status
    end,
  	o."descriptionFr",
  	o."descriptionNl",
  	o."descriptionEn",
  	o."infraManager",
  	o."isClub",
  	o."type name",
  	o."subtype name", 
  	o."subtype info",
  	o."reference key",
  	o."companyNumber",
  	o.vat,
  	o."legalName",
  	o."legalStatus",
  	o."contact name",
  	o."contact title",
  	o."contact email",
  	o."contact phone",
  	o.infrastructures,
  	array_to_json(array_agg(row_to_json(inf_items)) over (partition by o.id, place_items.id, place_geoms.id, act_items.id, aud_items.id)) as infrastructures_detailed,
  	o.places,
  	array_to_json(array_agg(row_to_json(place_items)) over (partition by o.id, inf_items.id, place_geoms.id, act_items.id, aud_items.id)) as places_detailed,
  	o."organisationActivities",
  	array_to_json(array_agg(row_to_json(act_items)) over (partition by o.id, inf_items.id, place_items.id, place_geoms.id, aud_items.id)) as activities_detailed,
  	o."organisationActivitiesAudiences",
  	array_to_json(array_agg(row_to_json(aud_items)) over (partition by o.id, inf_items.id, place_items.id, place_geoms.id, act_items.id)) as audiences_detailed,
  	st_union(place_geoms.geom) over (partition by o.id) as geom
from organisation o
	left join inf_items on inf_items.id = any(o.infrastructures)
	left join place_items on place_items.id = any(o.places)
	left join place_geoms on place_geoms.id = any(o.places)
	left join act_items on act_items.id = any(o."organisationActivities")
	left join aud_items on aud_items.id = any(o."organisationActivitiesAudiences");
GRANT SELECT ON TABLE sportkadaster.organisation_mvw TO perspective;



--------------------------------------
-- Place
--------------------------------------
-- drop materialized view place_mvw
create materialized view place_mvw as
with inf_items as (select distinct id, "nameFr", "nameNl", "nameEn" from infrastructure),
	 org_items as (select distinct id, "nameFr", "nameNl", "nameEn" from organisation),
	 place_geometries as (select distinct id, st_transform(ST_SetSRID(ST_MakePoint("urbisRef_x", "urbisRef_y"),4326), 31370) as geom from place)
select distinct on (p.id)
	p.id,
	p."nameFr",
	p."nameNl",
	p."nameEn",
	CASE status
    WHEN 'V' THEN 'Validated'
    ELSE p.status 
    END,
	p."streetFr",
	p."streetNl",
	p."number",
	p."postCode",
	p."city",
	p.address,
	sd.name_fr as statdistr_name_fr,
	sd.name_nl as statdistr_name_nl,
	sd.nis_district_code as statdistr_code,
	p."isUrbisAddress", 
	p."urbisRef_x",
	p."urbisRef_y",
	p.sector, 
	p."ownerType",
	p."isPublic", 
	p."isSchool",
	p."property_carparking_isAvailable",
	p."property_carSpace",
	p."property_carSpacePMR",
	p."property_carSpaceVIP",
	p."property_carSpaceBus",
	p."property_hasConvivialityArea",
	p."property_bikeparking_isAvailable",
	p."property_bikeparking_totalSpaces",
	p."property_bikeparking_isSecured",
	p."property_bikeparking_isFullyCovered",
	p.property_playground,
	p.infrastructures,
	array_to_json(array_agg(row_to_json(inf_items)) over (partition by p.id)) as infrastructures_detailed,
	p.organisations,
	array_to_json(array_agg(row_to_json(org_items)) over (partition by p.id)) as organisations_detailed,
	pg.geom
from place p
	left join inf_items on inf_items.id = any(p.infrastructures)
	left join org_items on org_items.id = any(p.organisations)
	left join place_geometries pg on pg.id = p.id
	left join bxl_statistical_district sd ON st_intersects(pg.geom, sd.geom)
	;
GRANT SELECT ON TABLE sportkadaster.place_mvw TO perspective;

--------------------------------------
-- Subsidy
--------------------------------------
-- drop materialized view subsidy_mvw;
create materialized view subsidy_mvw as 
select distinct on (s.id)
	s.id, 
	s."name",
	s."subsidy organisation",
	s."more information",
    CASE s.status
    WHEN 'N' THEN 'N-code: draft?'
	when 'V' then 'Validated'
	when 'E' then 'Exported'
	when 'L' then 'Legacy'
	when 'D' then 'Draft'
	when 'R' then 'Refused'
	when 'W' then 'Waiting for validation'
    ELSE s.status 
    END,
	s."date", 
	s."amount",
	s."modification date",
	s."operating subsidy",
	s."subsidy type", 
	s."starting date", 
	s."closing date", 
	s."contact",
	s."organisationMainId",
	o."nameFr" as organisation_nameFr,
	o."nameNl" as organisation_nameNl,
	o."nameEn" as organisation_nameEn,
	s."organisationSubsidyBpl",
	s."infrastructureId",
	i."nameFr" as infrastructure_nameFr,
	i."nameNl" as infrastructure_nameNl,
	i."nameEn" as infrastructure_nameEn
from subsidy s
	left join organisation o on s."organisationMainId" = o.id
	left join infrastructure i on s."infrastructureId" = i.id;
GRANT SELECT ON TABLE sportkadaster.subsidy_mvw TO perspective;


-- Par pouvoir subsidiante/subsidie verlenende authoriteit
-- nog filteren op basis van status
-- drop materialized view subsidy_grantor_mvw;
create materialized view subsidy_grantor_mvw as 
select
	s."subsidy organisation",
	extract(year from s."date") as year, 
	sum(s."amount") as amount
from subsidy s
	left join organisation o on s."organisationMainId" = o.id
	left join infrastructure i on s."infrastructureId" = i.id
group by s."subsidy organisation", extract(year from s."date")
order by s."subsidy organisation" asc, extract(year from s."date") desc;
GRANT SELECT ON TABLE sportkadaster.subsidy_grantor_mvw TO perspective;


-- par organisation qui reçoit la subside / per organisatie die de subsidie ontvangt
-- nog filteren op basis van status
-- drop materialized view subsidy_grantee_mvw;
create materialized view subsidy_grantee_mvw as 
select
	s."organisationMainId",
	o."nameFr" as organisation_nameFr,
	o."nameNl" as organisation_nameNl,
	extract(year from s."date") as year,
	sum(s.amount) as amount
from subsidy s
	left join organisation o on s."organisationMainId" = o.id
	left join infrastructure i on s."infrastructureId" = i.id
group by s."organisationMainId", o."nameFr", o."nameNl", extract(year from s."date")
order by o."nameFr" asc, extract(year from s.date);
GRANT SELECT ON TABLE sportkadaster.subsidy_grantee_mvw TO perspective;




--------------------------------------
-- Statistical districts
--------------------------------------
CREATE TABLE sportkadaster.bxl_statistical_district (
	id serial NOT NULL,
	id_statistical_district int2 NOT NULL,
	name_fr varchar(255) NOT NULL,
	name_nl varchar(255) NOT NULL,
	name_bil varchar(255) NULL,
	nis int2 NOT NULL,
	district_code varchar(255) NOT NULL,
	nis_district_code varchar(255) NOT NULL,
	geom geometry(MULTIPOLYGON, 31370) NOT NULL,
	CONSTRAINT bxl_statistical_district_pk PRIMARY KEY (id),
	CONSTRAINT bxl_statistical_district_un UNIQUE (id_statistical_district)
);
CREATE INDEX bxl_statistical_district_sidx ON sportkadaster.bxl_statistical_district USING gist (geom);

-- insert into sportkadaster.bxl_statistical_district select * from nova_2020.bxl_statistical_district;