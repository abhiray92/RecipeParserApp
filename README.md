</b>This is a simple application to parse raw csv files exported from a SCADA application. Although this application serves a pretty specific use case. It can still be used for various other purposes. This application has two components. </b>

<h3>Combine</h3>
This option will let one combine multiple recipe files in raw csv format and merge them into a tabular format for a particular parameter form factor (assuminng its Vials in this case). The table can be exported in either CSV or HTML file format.

An example of the exported html file - 

![image](https://github.com/abhiray92/RecipeParserApp/assets/42731567/e3cef3d6-2b31-4549-a5ec-364798a59dd1)


<h3>Compare</h3>
The compare option lets you compare a raw csv file with the combined CSV file generated above. It automatically selects the recipe (column) from the combined CSV file based on the details in the raw CSV file. The recipe is then transformed into a table and the difference in the values are highlighted. The 'Approved_value' column represents the column from the combined CSV file and the 'Actual_value' column is from the raw CSV file being compared.

A sample for the raw CSV file - 
```
PM-CONTROL: Produkt-/Rezeptsystem
2015-02-06;20:14



<begin>language
en
<end>language


<begin>recipe
#header;recipegroupname;name;parassign_name;number;parassign_number;state;shortname;parassign_shortname;endproductname;parassign_endproductname;version;parassign_version;date_of_release;parassign_date_of_release;release_person;parassign_release_person;builder;parassign_builder;builddate;parassign_builddate;changename;parassign_changename;changedate;parassign_changedate;normvalue;recipeoption;work_command;work_string;sequrity_command;sequrity_string;remark;user1;parassign_user1;user2;parassign_user2;user3;parassign_user3;user4;parassign_user4;user5;parassign_user5;user6;parassign_user6;user7;parassign_user7;user8;parassign_user8;user9;parassign_user9;user10;parassign_user10
#data;Filling;60R vial, 6.66ml pp;;60R vial, 6.66ml pp;;1;;;;;06;;2018-08-09 10:04:56;;james.doe;;genie.doe;;2017-12-18 16:58:34;;jack.doe;;2023-08-21 14:41:50;;1.000000;2;0;;0;;Created 18Dec2017 by AAA under Area-51;;;;;;;;;;;;;;;;;;;;
<begin>pe_recipe
#header;name;min_abs;min_rel;max_abs;max_rel;ordertime;scaletype;string;value
#data;Filling;-1.000000;100.000000;-1.000000;100.000000;0;0;;1.000000
<end>pe_recipe
<begin>paramgroup
#header;name;remark
#data;Capacity;
<begin>param
#header;name;type;operate_before;operate_online;value;unit;materialnumber;warehouse;scaletype;string;operate_limit;upper_limit;lower_limit;flags;is_material_param
#data;Machine capacity;2;0;0;9.000000;Stück/min;;;0;;0;;;0;0
<end>param
<end>paramgroup
<begin>paramgroup
#header;name;remark
#data;Infeed stroke movement;
<begin>param
#header;name;type;operate_before;operate_online;value;unit;materialnumber;warehouse;scaletype;string;operate_limit;upper_limit;lower_limit;flags;is_material_param
#data;Transport position;2;0;0;0.000000;mm;;;0;;0;;;0;0
#data;Upper position;2;0;0;17.700000;mm;;;0;;0;;;0;0
<end>param
<end>paramgroup
<begin>paramgroup
#header;name;remark
#data;Tub gripper;
<begin>param
#header;name;type;operate_before;operate_online;value;unit;materialnumber;warehouse;scaletype;string;operate_limit;upper_limit;lower_limit;flags;is_material_param
#data;Waiting position;2;0;0;-18.000000;mm;;;0;;0;;;0;0
#data;Pick up position;2;0;0;-27.000000;mm;;;0;;0;;;0;0
#data;Unclamping pos.;2;0;0;-25.000000;mm;;;0;;0;;;0;0
<end>param
<end>paramgroup
<begin>paramgroup
#header;name;remark
#data;Lid foil module transport;
<begin>param
#header;name;type;operate_before;operate_online;value;unit;materialnumber;warehouse;scaletype;string;operate_limit;upper_limit;lower_limit;flags;is_material_param
#data;Speed tub transport ;2;0;0;20.000000;%;;;0;;0;;;0;0
#data;Speed transport tub at peeling module;2;0;0;5.000000;%;;;0;;0;;;0;0
<end>param
<end>paramgroup
<end>recipe
```

Sample of the HTML file comparing two tables - 

![image](https://github.com/abhiray92/RecipeParserApp/assets/42731567/d9b0bd66-0e65-4542-a2fe-ebda24f2dedf)

This is just a sample output, the values may not refer to the exact value in the above tables.
