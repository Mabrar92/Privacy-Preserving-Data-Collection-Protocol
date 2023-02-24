# Enhanced Privacy Preserving Data Collection Protocol for 1:M Dataset

This is the offcial Implementation of [Privacy-Preserving Data Collection for IoT based 1: M Datasets](https://link.springer.com/article/10.1007/s11042-021-10562-3) as part of my final Year thesis for Masters in Software Engineering under the supervision of Dr.Adeel Anjum from Comsats University Islamabad Pakistan.
The code is written in python 3.0.


### Instructions:

#### `Eppdc.py is the main module which takes the following Arguments;` 

                                                            Dataset[a|i] Attributes[7|14]   Partitions{p} Counterfeit_Sensitive_Values [CSI]
                                                                       |              |             |                  |
                                                                       |              |             |                  |
                                                                       |              |             |                  |
                                                                       |              |             |                  |
                                                                       v              |             |                  |
                                                   Adult dataset | Informs dataset    |             |                  |
                                                                                      v             |                  |
                                                         Number of Attributes for Chosen dataset    |                  |
                                                                                                    v                  |
                                                               Number of l-diverse groups for chosen dataset           |  
                                                                                                                       v
                                                                       Number of Counterfeit Sensitive Values provided to Second Leader by Dataholders

### `Sample Command Line Usage : python Eppdc.py a 7 50 2`

### OutPut FIles
#### `All data.xlsx`
#### `MST_Table.xlsx` 
#### `SLandFL_datasets.xlsx`

