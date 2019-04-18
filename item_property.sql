CREATE SEQUENCE IF NOT EXISTS public.item_property_id_seq;
CREATE TABLE IF NOT EXISTS public.item_property(
item_number varchar(27) NOT NULL DEFAULT nextval('item_property_id_seq'::regclass),	
brand_id integer NOT NULL,
prodline_id integer,
life_puppy integer,
life_kitten integer,
life_adult integer,
breed_small integer,
breed_large integer,
type_food integer,
type_toy integer,
type_litter integer,
type_medication integer,
texture_dry integer,
texture_wet integer,
cost_lt_10 integer,
cost_10_19 integer,
cost_20_29 integer,
cost_30_39 integer,
cost_40_49 integer,
cost_50_59 integer,
cost_60_69 integer,
cost_70_100 integer,
cost_gt_100 integer,
cost_gt_250 integer,
cost_gt_500 integer,
cost_gt_1000 integer,
specie_dog integer,
specie_cat integer,
specie_other integer,
texture_raw integer,
CONSTRAINT item_property_pkey PRIMARY KEY(item_number))
WITH (
OIDS = FALSE
)
TABLESPACE pg_default;
										   
ALTER SEQUENCE item_property_id_seq
OWNED BY item_property.item_number;	
