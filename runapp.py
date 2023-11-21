import streamlit as st

st.title('Welcome to Lucy Number by Name')
name = st.text_input('What is your full name? ')
name_without_space = name.replace(' ', '')
ntl = list(name_without_space)
into_numbers = []
for letter in ntl:
    into_numbers.append(ord(letter))
    big_num = sum(into_numbers)
    big_num_str = str(big_num)
    num2 = 0
    num3 = 0
    num = 0
    for char in big_num_str:
        num2 += int(char)
    if num2 > 9:
        num2_str = str(num2)
        for char in num2_str:
            num3 += int(char)
            num = num3

    else:
        num = num2
    if num > 9:
        num_str = str(num)
        num = 0
        for char in num_str:
            num += int(char)

print(num)

if name:
    st.write(f"your Name is {name} and your Special Lucy Number is {num} ")
