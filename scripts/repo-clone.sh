#!/bin/bash

service_name=$1

# Verificar si el directorio existe
if [ -d "tmp/repos/$service_name" ]; then
    echo "El directorio tmp/repos/$service_name/ existe. Eliminando..."
    rm -rf "tmp/repos/$service_name"
    echo "Directorio eliminado."
fi

gh repo clone occmundial/$service_name tmp/repos/$service_name/