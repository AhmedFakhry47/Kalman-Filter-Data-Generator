# Kalman-Filter-Data-Generator
Python script to generate data for kalman filter , data include measurements from Lidar and Radar sensors in addition to GroundTruth values for 6 state variables Position_X,Position_Y , Vx , Vy , Yaw , Yaw rate ( rotational velocity)

Notes :
• Al values are in meters

• Data generation done for constant turn rate and constant velocity ( That can be changed )

• turn rate = .55 radian/sec but it can be changed , same as linear velocity 

• Lidar measurements error covariance matrix is [[.15 0] , [0 .15]]

• Radar measurements error covariance matrix is [ [.3 0 0 ] , [0 .03 0] , [0 0 .3] ]

-Running the code is so simple , just change the save path inside the code and run it 

-Another script (val.py) is used to plot Position_X , Position_Y measurements from Lidar and Radar in addition to the groundtruth Positions. 


