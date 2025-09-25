# *******************************************************************************
# OpenStudio(R), Copyright (c) Alliance for Sustainable Energy, LLC.
# See also https://openstudio.net/license
# *******************************************************************************

require 'openstudio/replace_refrigerant/version'
require 'openstudio/extension'

module OpenStudio
  module ReplaceRefrigerant
    class ReplaceRefrigerant < OpenStudio::Extension::Extension
      # Override parent class
      def initialize
        super

        @root_dir = File.absolute_path(File.join(File.dirname(__FILE__), '..', '..'))
      end
    end
  end
end
