# Quantum-Scholars-Hackathon

Problem Set 1 Question 3 Screenshot
![Problem Set 1 Question 3 Screenshot](image1.png)

Problem Set 2 Question 3
(i) Let n be small (say less than 10). Running the protocol 10 times, is Eve detected in every case?

    No, Eve is not detected in every case. Since n is small, there is higher chance that Eve could guess the state of the bits that Alice sent.
    
(ii) Let n be large (say more than 1000). Running the protocol 10 times, is Eve detected in every case?

    Yes, Eve is detected in every case. Since n is large, the probability that Eve guesses the correct state of the bits that Alice sent is so small that she is basically guaranteed to get detected in every trial.
    
(iii) Based on your observations in cases when Eve is not detected what would you guess is the expected length of SK in terms of n?

    I would guess that the expected length of SK is about n/2 because t is generated randomly so that half of the bits should be 1 and half of the bits should be 0.

Problem Set 3 Question 3

(h) ![Histogram r = 1](image2.png)

(i) ![Histogram r = 3](image3.png)

(j) As seen in the two histograms, when r = 1 the marked state 1011 is already measured more frequently than the other states, but with r = 3 = ⌊π√N/4⌋ the marked state dominates even more dramatically, with all other states being nearly zero. This visually confirms that r = 3 is considerably better.