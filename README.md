
# Video Identification Based on Encrypted Network Traces and Attack Mitigation

In an era marked by escalating digital privacy concerns, the advent of side-channel attacks poses a substantial risk to the confidentiality of streaming service users. This project explores a novel method for identifying the specific YouTube videos users are watching, even when network traffic encryption is in place. The attack leverages side-channel analysis, focusing on the byte sizes of Hypertext Transfer Protocol (HTTP) requests exchanged between a user's browser and YouTube's servers.

## Objective

The primary objective of this research is to assess the feasibility of detecting YouTube videos using high-level network data from application logs. This project examines various machine learning models and statistical methods to identify fingerprinted YouTube videos in an open-world scenario where most examples are unknown.

## Methodology

Our research explores the potential for identifying YouTube videos by analyzing network traces at the application layer of the OSI model. Despite network encryption rendering traditional video identification methods ineffective, this project demonstrates that videos can still be identified by analyzing patterns in the sizes of data packets traveling through the network.

## Results

The findings reveal that it is indeed possible to identify YouTube videos with an impressive F1-Score of 80% in an open-world scenario. Furthermore, it demonstrates the capability to distinguish known and unknown videos with a recall rate of 92% within the same open-world scenario.

## Conclusion

The outcomes of this research underscore the urgency of enhanced security measures in response to the looming threat of side-channel attacks on network traffic traces. This project is a significant step forward in understanding and mitigating the privacy risks associated with streaming content delivery, especially in the context of Dynamic Adaptive Streaming over HTTP (DASH) techniques.



## Getting started
The *src* directory contains the systems involved in our practicum, that being the DataHarvesting, the AttackScenario, the Condenser, and the Youtube Modelling and Analysis. This repository contains an amalgam of multiple repositories used during the practicum. Feel free to replicate our research. To get started, download the dataset from [kaggle](https://tbd).

Create a virtual environment

```
python3 -m venv myenv 
source myenv/bin/activate
```

Start the harvasting data by adding the desired URLS of youtube videos to the all_urls.txt file 
```bash
cd src/dataharvesting
pip install -r requirements.txt
```

All models and notebooks for analysis are in the folder src/modelingandanalysis/youtube_video_detector. 


Feel free to reach out if any questoins arise!



