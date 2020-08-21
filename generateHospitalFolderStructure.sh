#!/bin/bash

mkdir hospital_System_A hospital_System_B hospital_System_C

hospitalSystemA=( Hospital1, Hospital2, Hospital3 )
for hospital in "${hospitalSystemA[@]}"
  do  
    mkdir hospital_System_A/$hospital && chmod 777 hospital_System_A/$hospital
  done

hospitalSystemB=( Hospital1, Hospital2 )
for hospital in "${hospitalSystemB[@]}"
  do  
    mkdir hospital_System_B/$hospital && chmod 777 hospital_System_B/$hospital
  done

hospitalSystemC=( Hospital1 )
for hospital in "${hospitalSystemC[@]}"
  do  
    mkdir hospital_System_C/$hospital && chmod 777 hospital_System_C/$hospital
  done
