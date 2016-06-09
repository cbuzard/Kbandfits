# Kbandfits 
This repository contains code to normalize brown dwarf K band spectra and fit it in portions to lines. 

montecarlotest_2 defines function to fit K bands:
  Input:
    Either source id and spectral id (from BDNYC database)
    Or textfile
    Optional- spectral type, SNR
  Output:
    slopesvals list with source id, spectral id, blue slope, standard deviation of blue slope, red slope, standard deviation of red slope, spectral type, filename
