from first_tone_based import first_tone_based
from relative_tone_based import relative_tone_based
from absolute_tone_based import absolute_tone_based
from cosine_similarity import cosine_similarity_custom
from cosine_similarity import final_similarity
from process_midi import normalize_length
import numpy as np

file_path = 'peter1.mid'
try:
    ATB = absolute_tone_based(file_path)
    print("ATB: ", ATB)
    RTB = relative_tone_based(file_path)
    print("RTB: ", RTB)
    FTB = first_tone_based(file_path)
    print("FTB: ", FTB)  

    file_path_two = 'peter2.mid'
    atb = absolute_tone_based(file_path_two)
    print("ATB 2: ", atb)
    rtb = relative_tone_based(file_path_two)
    print("RTB 2: ", rtb)
    ftb = first_tone_based(file_path_two)
    print("FTB 2: ", ftb)

    RTB, rtb, FTB, ftb = normalize_length(RTB, rtb, FTB, ftb)

    atbb = cosine_similarity_custom(ATB, atb)
    rtbb = cosine_similarity_custom(RTB, rtb)
    ftbb = cosine_similarity_custom(FTB, ftb)

    print("Cosine Similarity ATB: ", atbb)
    print("Cosine Similarity RTB: ", rtbb)
    print("Cosine Similarity FTB: ", ftbb)
    print("Final Similarity: ", final_similarity(atbb, rtbb, ftbb))

except Exception as e:
    print(f"Error: {e}")