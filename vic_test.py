# python3 manage.py shell

from core.models import Vic_scaling, Vic_atar  
from core.utility.atar_calculate_main import vic_study_score_to_scaled_score, vic_aggregate_to_atar  


scaled_score = vic_study_score_to_scaled_score("Accounting", 40.0)
print(f"Scaled score for Accounting with a study score of 40.0 is: {scaled_score}")

scaled_score = vic_study_score_to_scaled_score("Accounting", 40)
print(f"Scaled score for Accounting with a study score of 40 is: {scaled_score}")

scaled_score = vic_study_score_to_scaled_score("Accounting", 42)
print(f"Scaled score for Accounting with a study score of 42 is: {scaled_score}")

scaled_score = vic_study_score_to_scaled_score("Accounting", 36.6)
print(f"Scaled score for Accounting with a study score of 36.6 is: {scaled_score}")

scaled_score = vic_study_score_to_scaled_score("Accounting", 19)
print(f"Scaled score for Accounting with a study score of 19 is: {scaled_score}")

scaled_score = vic_study_score_to_scaled_score("Accounting", 0)
print(f"Scaled score for Accounting with a study score of 0 is: {scaled_score}")

scaled_score = vic_study_score_to_scaled_score("Accounting", 51)
print(f"Scaled score for Accounting with a study score of 51 is: {scaled_score}")

scaled_score = vic_study_score_to_scaled_score("Accounting", -0.1)
print(f"Scaled score for Accounting with a study score of -0.1 is: {scaled_score}")

scaled_score = vic_study_score_to_scaled_score("VCE VET Business", 21.86)
print(f"Scaled score for VCE VET Business with a study score of 21.86 is: {scaled_score}")

scaled_score = vic_study_score_to_scaled_score("Mathematics", 25)
print(f"Scaled score for Mathematics with a study score of 25 is: {scaled_score}")



atar_score = vic_aggregate_to_atar(198)
print(f"ATAR score for an aggregate of 198 is: {atar_score}")

atar_score = vic_aggregate_to_atar(198.5)
print(f"ATAR score for an aggregate of 198.5 is: {atar_score}")

atar_score = vic_aggregate_to_atar(200)
print(f"ATAR score for an aggregate of 200 is: {atar_score}")

atar_score = vic_aggregate_to_atar(230)
print(f"ATAR score for an aggregate of 230 is: {atar_score}")

atar_score = vic_aggregate_to_atar(211.18)
print(f"ATAR score for an aggregate of 211.18 is: {atar_score}")

atar_score = vic_aggregate_to_atar(231)
print(f"ATAR score for an aggregate of 231 is: {atar_score}")

atar_score = vic_aggregate_to_atar(65.65)
print(f"ATAR score for an aggregate of 66.65 is: {atar_score}")

atar_score = vic_aggregate_to_atar(65.66)
print(f"ATAR score for an aggregate of 65.66 is: {atar_score}")

atar_score = vic_aggregate_to_atar(-1)
print(f"ATAR score for an aggregate of -1 is: {atar_score}")

atar_score = vic_aggregate_to_atar(0)
print(f"ATAR score for an aggregate of 0 is: {atar_score}")

atar_score = vic_aggregate_to_atar(99)
print(f"ATAR score for an aggregate of 99 is: {atar_score}")
