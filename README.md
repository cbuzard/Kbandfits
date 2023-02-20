# Kbandfits 
In this project, I analyzed infrared data from brown dwarfs to reveal how prevalent water and CO absorption was at different temperatures and pressures. To do so, I normalized low resolution brown dwarf K-band spectra and performed linear fits to the spectral portions absorbed by various molecular species. I used a Monte Carlo analysis to estimate the error on the linear fits. 

montecarlotest_2 defines function to fit K bands:

  Input:
  
    Either source id and spectral id (from BDNYC database)
    
    Or textfile
    
    Optional- spectral type, SNR
    
  Output:
  
    slopesvals list with source id, spectral id, blue slope, standard deviation of blue slope, red slope, standard deviation of red slope, spectral type, filename
