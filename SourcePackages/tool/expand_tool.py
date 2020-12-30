

def remove_symbol(input_str):
    input_str = input_str.replace("、","")
    input_str = input_str.replace("。", "")
    input_str = input_str.replace("，", "")
    input_str = input_str.replace("：", "")
    input_str = input_str.replace("？", "")
    input_str = input_str.replace("-", "")
    input_str = input_str.replace(" ","")
    return input_str



if __name__ == "__main__":
    print("finished")