
# OpenStudio Refrigerant Replacement

## Overview
This repository provides an OpenStudio/EnergyPlus Measure developed at **Oak Ridge National Laboratory (ORNL)** to support the use of alternative refrigerants in building energy models.  
The measure enables users to **add or replace refrigerants** in EnergyPlus models with updated property data.  
Currently, it supports **R448A** and **R449A**, both of which are non-flammable A1 safety-class refrigerants intended as replacements for R404A or R22 in commercial refrigeration systems.

## Background

This Measure extends OpenStudio and EnergyPlus by letting users introduce new refrigerants without modifying source code. Currently, reference data for refrigerant fluid properties (FluidPropertiesRefData.idf) are provided in the form of a dataset that includes R-11, R-12, R-22, R-123, R-134a, R-404A, R-407A, R-410A, NH3, R-507A, and R-744, so evaluating alternative refrigerants required manual file edits that were error prone and time consuming.

OpenStudio Measures are a scripting facility based on Ruby or Python to automate model changes and to incrementally extend and customize the OpenStudio platform. Model measures inherit from `openstudio.measure.ModelMeasure` and EnergyPlus measures inherit from `openstudio.measure.EnergyPlusMeasure`.

Although OpenStudio Measures grant access to the entire OpenStudio model, they do not include the EnergyPlus data model. EnergyPlus Measures provide access to the EnergyPlus data model. This Measure is intended to run after the OSM has been translated to EnergyPlus. In EnergyPlus Measures, the run and arguments methods use a workspace argument instead of a model argument, where workspace refers to the EnergyPlus Workspace.

## Repository Structure
- **measure.py** – Main Python script implementing the EnergyPlus Measure. Defines user arguments and refrigerant replacement logic.  
- **measure.xml** – Metadata defining measure schema, arguments, and tool compatibility.  
- **resources/FluidPropertiesRefData_R448a.idf** – Refrigerant property dataset for R448A.  
- **resources/FluidPropertiesRefData_R449a.idf** – Refrigerant property dataset for R449A.  
- **resources/R448A449A_MT_LT_Curves.idf** – Compressor performance curves for R448A and R449A (medium- and low-temperature applications).

See [resources/README.md](replace_refrigerant/resources/README.md) for dataset details and generation notes.

## Measure Description


## Example

## License
This is a work in progress and will be distributed under the terms of the BSD-3-Clause license
