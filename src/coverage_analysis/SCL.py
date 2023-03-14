
IND_LABELS_ = {
    0: "NO_DATA",
    1: "SATURATED_OR_DEFECTIVE",
    2: "DARK_AREA_PIXELS",
    3: "CLOUD_SHADOWS",
    4: "VEGETATION",
    5: "NOT_VEGETATED",
    6: "WATER",
    7: "UNCLASSIFIED",
    8: "CLOUD_MEDIUM_PROBABILITY",
    9: "CLOUD_HIGH_PROBABILITY",
    10: "THIN_CIRRUS",
    11: "SNOW",
}

LABEL_IND_ = {v: k for k,v in IND_LABELS_.items()}

IND_CLOUDS_ = [3, 8, 9] #[k for k,v in IND_LABELS_.items() if "CLOUD" in v]
IND_ALL_ = list(IND_LABELS_.keys())

def remove_labels(source: list, labels_to_remove: list):
    if type(source) == list and type(labels_to_remove) == list:
        return [v for v in source if v not in labels_to_remove]
    else:
        print("Not list inputs, therefore removing is not performed")
        return source