
# *****************************************************************************
#   GLOBAL
# *****************************************************************************

.PHONY: clean

MAKEFILE_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))

# Cleanup up downloaded and exported files
clean:
	rm -rf ./bin ./png ./svg


# *****************************************************************************
#   PLANTUML JAR
# *****************************************************************************

# If the JAR file isn't already present, download it
PLANTUML_JAR     := $(MAKEFILE_DIR)/bin/plantuml.jar
PLANTUML_JAR_URL := https://sourceforge.net/projects/plantuml/files/plantuml.jar/download
bin/plantuml.jar:
	curl -sSfL $(PLANTUML_JAR_URL) -o $(PLANTUML_JAR) --create-dirs


# *****************************************************************************
#   DIAGRAMS & IMAGE EXPORT FORMATS
# *****************************************************************************

# Source PlantUML diagram files
DIAGRAMS_SRC := $(notdir $(wildcard *.puml))

define IMAGE_EXPORT_FORMAT
# Define image output file list
DIAGRAMS_$1 := $(addprefix $1/, $(addsuffix .$1, $(basename $(DIAGRAMS_SRC))))
# Define image filetype target
$1: bin/plantuml.jar $$(DIAGRAMS_$1)
# Recipe to export a filetype
$1/%.$1: %.puml
	java -jar $(PLANTUML_JAR) -charset UTF-8 -t$1 $$^ -o $1/ $2
endef

# Default target first; build PNGs, probably what we want most of the time
$(eval $(call IMAGE_EXPORT_FORMAT,png,-Sdpi=300 -DPLANTUML_LIMIT_SIZE=8192))
$(eval $(call IMAGE_EXPORT_FORMAT,svg))
