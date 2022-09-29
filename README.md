# KNOWM memristors in delay based Reservoir Computing system for epilepsy recognition

## Summary
In this study, hardware KNOWM memristors were used to transform signals to improve F0-score of epilepsy classification. Four connected memristors served as single computational node. Reservoir Computing setup with delayed feedback loop was used to gradually increase the degree of transformation of the signal. Transformation of signal occurs because of nonlinear electric response of memristors. In result, changes in Pearson correlation and distribution of features along with data expansion allowed to increase the F0-score of classification of epilepsy seizure for small datasets.

Link to study: https://www.tandfonline.com/doi/abs/10.1080/17445760.2022.2088751?journalCode=gpaa20

### General workflow
- test and characterize the setup with simple waveforms (sin, square, triangle)
- calculate Fast Fourier Transforms for Total Harmonic Distortion parameter for obtained signals
- prepare the main dataset
- apply proper signal and record the response of the system
- handle experimental data
- test stationarity of timeseries
- calculate complexity parameters (serving as features) for raw and transformed signals
- spot-check algorithms and choose the classifier
- train/test model on the basis of raw and transformed signals
- compare results, propose explanations for the differences

#### Dataset

Dataset was acquired with tri-axial accelerometer worn on the wrist during epilepsy seizure and three control activities: walking, running and sawing. It consist of timeseries of equal length.

Dataset was taken from: https://www.timeseriesclassification.com/description.php?Dataset=Epilepsy

### References

Parts of code were inspired by https://machinelearningmastery.com/ course. I recommend it!

