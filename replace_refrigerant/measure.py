import typing
import openstudio
import os
from pathlib import Path
fp=Path(__file__).parent.resolve()
class AddRefrigerant(openstudio.measure.EnergyPlusMeasure):
    """An EnergyPlusMeasure."""
    
    def name(self):
        return "Add refrigerant to the model"

    def description(self):
        return "Measures that adds selected refrigerant to the model"

    def modeler_description(self):
        return "Add selected refrigerant fluid to the openstudio file using the EnergyPlusMeasure"
    
    def dummy_method(self):
        pass
    
    def arguments(self, workspace: openstudio.Workspace):
        """Prepares user arguments for the measure.
        Measure arguments define which -- if any -- input parameters the user may set before running the measure.
        """
        args = openstudio.measure.OSArgumentVector()
        
        """Choice argument for new refrigerant"""
        refrigerant_chs=openstudio.StringVector()
        refrigerant_chs.append("R448a")
        refrigerant_chs.append("R449a")
        Refrigerant=openstudio.measure.OSArgument.makeChoiceArgument("Refrigerant",refrigerant_chs)
        Refrigerant.setDisplayName("Name of new refrigerant")
        Refrigerant.setDescription("This will refer to the corresponding idf file where the data for the refrigerant is located")
        Refrigerant.setDefaultValue("R448a")
        args.append(Refrigerant)
        
        
        #Add_refrigerant=openstudio.measure.OSArgument.makeBoolArgument("Add_refrigerant")
        #Refrigerant.setDisplayName("Add refrigerant to model?")
     
        
        
        
        
        """Choice arguments for objects whose refrigerant should be replaced"""
        objects_with_refrigerant= ["Refrigeration:System",
                                   "Refrigeration:TranscriticalSystem",
                                   "Refrigeration:SecondarySystem", 
                                   "Coil:Cooling:WaterToAirHeatPump:ParameterEstimation",
                                   "Coil:Heating:WaterToAirHeatPump:ParameterEstimation",
                                   "AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl",
                                   "AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:HR"]
        replace_obj=openstudio.StringVector()
        for element in objects_with_refrigerant:
            replace_obj.append(element)
        replace_obj.append("All")
        Objects_for_replacement=openstudio.measure.OSArgument.makeChoiceArgument("Objects_for_replacement",replace_obj)
        Objects_for_replacement.setDisplayName("Objects to replace replacement")
        Objects_for_replacement.setDescription("Selec the objects for which the refrigerant should be replaced with new refrigerant")
        Objects_for_replacement.setDefaultValue("All")
        args.append(Objects_for_replacement)
        
        Refrigerant_to_be_replaced=openstudio.measure.OSArgument.makeStringArgument("Refrigerant_to_be_replaced",True)
        Refrigerant_to_be_replaced.setDisplayName("Refrigerant to be replace")
        Refrigerant_to_be_replaced.setDescription("If a specific refrigerant is to be replaced, then enter the name of the refrigreation, else all the refrigerant will be replaced")
        Refrigerant_to_be_replaced.setDefaultValue("All")
        args.append(Refrigerant_to_be_replaced)
        
        
        
        return args
# =============================================================================
#     def read_idf(self,workspace:openstudio.Workspace, path: openstudio.path):
#         file=path("FluidPropertiesRefData_R448a")
# =============================================================================
        
        
    def run(
        self,
        workspace: openstudio.Workspace,
        runner: openstudio.measure.OSRunner,
        user_arguments: openstudio.measure.OSArgumentMap,
    ):
        """Defines what happens when the measure is run."""
        super().run(workspace, runner, user_arguments)  # Do **NOT** remove this line

        #if not (runner.validateUserArguments(self.arguments(workspace), user_arguments)):
            #return False
        
        
        """assign the user inputs to variables"""
        Refrigerant = runner.getStringArgumentValue("Refrigerant", user_arguments)
        Objects_for_replacement= runner.getStringArgumentValue("Objects_for_replacement", user_arguments)
        Refrigerant_to_be_replaced = runner.getStringArgumentValue("Refrigerant_to_be_replaced", user_arguments)
        
        """base on variable selected load the idf file and get refrigerant_workspace which is different from workspace of the osm model """
        refrigerant_idf_filepath=openstudio.path(os.path.dirname(os.path.abspath(__file__))+"\\resources\\FluidPropertiesRefData_"+Refrigerant+".idf")
       
        refrigerant_workspace=openstudio.Workspace.load(refrigerant_idf_filepath).get()  
        
        if not refrigerant_workspace:
          runner.registerError("Failed to load the idf file with refrigerant objects as workspace")
          return False
       
        """copy the objects from refrigerant workpspace to workspace"""
        ref_obj=refrigerant_workspace.objects()
        workspace.addObjects(ref_obj,False) #False is to not check for conflicts
        
        """prepare a dictionary with objects for which the changes has to be done as keys and index of the field as value"""
        refrigerant_objects_dict = {"Refrigeration:System":6, #Refrigeration System Working Fluid Type
                                    "Refrigeration:TranscriticalSystem":9,
                                    "Refrigeration:SecondarySystem":3,
                                    "Coil:Cooling:WaterToAirHeatPump:ParameterEstimation":2,
                                    "Coil:Heating:WaterToAirHeatPump:ParameterEstimation":2,
                                    "AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl":3,
                                    "AirConditioner:VariableRefrigerantFlow:FluidTemperatureControl:HR":3}
    
        """Replace the old refrigerant for all the objects listed above with new refrigerant"""
        if Objects_for_replacement=="All":   
            for obj_type in refrigerant_objects_dict.keys():
                index= refrigerant_objects_dict[obj_type]
                for obj in workspace.getObjectsByType(obj_type):  
                    if Refrigerant_to_be_replaced == "All":
                        """Replace all refrigerant in each of the objects"""
                        obj.setString(index,Refrigerant)
                         
                    else:
                        """Replace if existing refrigeratn in object is same as user selected refrigerant ( like R-134A, R-32, etc) """
                        if Refrigerant_to_be_replaced ==obj.getString(index):
                            obj.setString(index,Refrigerant) 
        
        else:
            """Replace one of the objects replaced for replacement"""
            for obj_type in refrigerant_objects_dict.keys():
                if obj_type==Objects_for_replacement:
                    index= refrigerant_objects_dict[obj_type]
                    for obj in workspace.getObjectsByType(obj_type):
                        if Refrigerant_to_be_replaced == "All":
                            """Replace all refrigerant in each of the objects"""
                            obj.setString(index,Refrigerant)
                        else:
                            """Replace if existing refrigeratn in object is same as user selected refrigerant ( like R-134A, R-32, etc) """
                            if Refrigerant_to_be_replaced ==obj.getString(index):
                                obj.setString(index,Refrigerant)              
        
        if Objects_for_replacement=="Refrigeration:System" or Objects_for_replacement=="All": #Change the power and capacity curve if replacement is for "Refrigeration:System"
            for obj in workspace.getObjectsByType("Refrigeration:System"):
                case_list_name=obj.getString(1).get()        
                compressor_list_name=obj.getString(4).get() 
    
                compressor_list = workspace.getObjectByTypeAndName("Refrigeration:CompressorList",compressor_list_name).get()
                #print(compressor_list.get())
                case_list = workspace.getObjectByTypeAndName("Refrigeration:CaseAndWalkInList",case_list_name).get()
                #print(case_list.get())
    
                first_case_walkin_name = case_list.getString(1).get()
    
    
                #first_case=workspace.getObjectByTypeAndName("Refrigeration:Case",first_case_walkin_name).get()
                cases=workspace.getObjectsByType("Refrigeration:Case")
                walkins=workspace.getObjectsByType("Refrigeration:WalkIn")
                compressors=workspace.getObjectsByType("Refrigeration:Compressor")
                
                case_found=False
                for Case in cases:
                    if Case.getString(0).get()==first_case_walkin_name:
                        operating_temperature=float(Case.getString(9).get())
                        case_found=True
                        break
                if not case_found:
                    for walkin in walkins:
                        if walkin.getString(0).get()==first_case_walkin_name:
                            operating_temperature=float(walkin.getString(3).get())
                            break
                compressor_namelist=[]
                for i in range(1,compressor_list.numFields()):
                    compressor_name=compressor_list.getString(i).get()
                    compressor_namelist.append(compressor_name)
                
                for compressor in compressors:
                    if compressor.nameString() in compressor_namelist:
                        if operating_temperature > -18:
                            compressor.setString(1,"R448A449A_MT_Power")
                            compressor.setString(2,"R448A449A_MT_Capacity")
                        else:
                            compressor.setString(1,"R448A449A_LT_Power")
                            compressor.setString(2,"R448A449A_LT_Capacity")
        return True


# register the measure to be used by the application
AddRefrigerant().registerWithApplication()
