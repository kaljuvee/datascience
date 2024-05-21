from extractor import convert_to_df

def test_convert_to_df():
    sample_table = """
    | Medication | Ordered Dose/Rate | Route | Frequency | Last Action |
    |------------|-------------------|-------|-----------|-------------|
    | acetaminophen | 975 mg | oral | Q8H | Given, 975 mg at 04/04 0530 |
    | aspirin ec | 81 mg | - | - | Given, 81 mg at 04/04 0922 |
    | atorvastatin (LIPITOR) | 80 mg | - | - | Given, 80 mg at 04/03 |
    | cyanocobalamin (vitamin B-12) | 1,000 mcg | - | - | Given, 1,000 mcg at 04/04 0921 |
    | donepezil (ARICEPT) | 5 mg | oral | QD | Given, 5 mg at 04/04 0922 |
    | fluticasone propionate (FLONASE) | 1 spray | nasal spray | BID | Given, 1 spray at 04/04 |
    | Folic acid (FOLVITE) | 1,000 mcg | Oral | QAM | Given, 1,000 mcg at 04/04 0921 |
    | levothyroxine (SYNTHROID, LEVOTHROID) | 37.5 mcg | oral | 2x weekly | Ordered |
    | levothyroxine (SYNTHROID, LEVOTHROID) | 75 mcg | oral | 5x weekly | Given, 75 mcg at 04/04 0530 |
    """
    try:
        df = convert_to_df(sample_table)
        print(df)
        df.to_csv("test.csv", index=False)
        print("Test Passed: DataFrame converted successfully")
    except Exception as e:
        print(f"Test Failed: {e}")

if __name__ == "__main__":
    test_convert_to_df()
