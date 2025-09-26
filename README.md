# Replace Refrigerant Gem

This gem is used to replace refrigerant in Openstudio model with alternative refrigerant. The details of the Openstudio measure is available at [Documentation](lib/measures/OpenStudio_replace_refrigerant/Readme.md)

## Installation

Add this line to your application's Gemfile:

```ruby
gem 'OpenStudio-replace-refrigerant'
```

And then execute:

    $ bundle

Or install it yourself as:

    $ gem install 'OpenStudio-replace-refrigerant'

## Usage

This gem is used for adding/replacing the refrigerants in OpenStudio model with alternative refrigerant R448A and R449A  

## TODO

- [ ] Remove measures from OpenStudio-Measures to standardize on this location
- [ ] Update measures to code standards
- [ ] Review and fill out the gemspec file with author and gem description

# Releasing

* Update change log
* Update version in `/lib/openstudio/OpenStudio-replace-refrigerant/version.rb`
* Merge down to master
* Release via github
* run `rake release` from master

# License
This is a work in progress and will be distributed under the terms of the BSD-3-Clause license
