
# OpenStudio Refrigerant Replacement

## Fluid Properties Generation
The refrigerant fluid property datasets (`FluidPropertiesRefData_R448a.idf` and `FluidPropertiesRefData_R449a.idf`) were generated using **NIST Reference Fluid Thermodynamic and Transport Properties Database (REFPROP): Version 10** data.  

- Properties include thermodynamic values across saturation and superheated regions.  
- Data were sampled across representative temperature and pressure ranges for use in EnergyPlus.  
- Converted into EnergyPlus IDF format so they can be automatically imported into a model during Measure execution.  

## Performance Curve Generation
The **compressor performance curves** for R448A and R449A were generated using **actual manufacturer compressor datasets**

- Source data: Manufacturer compressor maps for R448A and R449A. Capacity (Q) and power (W) as functions of suction temperature (SST) and condensing temperature (SCT), with separate datasets for MT and LT ranges.
- Fitting method: Two-dimensional bicubic polynomial regression in SST and SCT, estimated using ordinary least squares (EnergyPlus `Curve:Bicubic`).
- Validation and export: Fitted surfaces exported as EnergyPlus IDF curve objects in `resources/R448A449A_MT_LT_Curves.idf`, with each curve annotated with SST and SCT minimum and maximum bounds.  
 `Curve names: R448A449A_MT_Capacity, R448A449A_MT_Power, R448A449A_LT_Capacity, R448A449A_LT_Power.`

## License
This is a work in progress and will be distributed under the terms of the BSD-3-Clause license