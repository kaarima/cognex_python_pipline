import socket
import csv
import time


IP = "192.168.10.5"
PORT = 23


# ==============================
# Cognex spreadsheet cells
# ==============================

CELLS = {

    # X distances
    "DX12": "C32",
    "DX23": "C33",
    "DX34": "C34",
    "DX56": "C35",
    "DX25": "C36",


    # Y distances
    "DY12": "C81",
    "DY23": "C82",
    "DY34": "C83",
    "DY56": "C84",
    "DY66": "C85",



    # Blob 1
    "B1_Row": "C61",
    "B1_Col": "C62",
    "B1_Area": "C63",

    # Blob 2
    "B2_Row": "C64",
    "B2_Col": "C65",
    "B2_Area": "C66",

    # Blob 3
    "B3_Row": "C67",
    "B3_Col": "C68",
    "B3_Area": "C69",

    # Blob 4
    "B4_Row": "C70",
    "B4_Col": "C71",
    "B4_Area": "C72",

    # Blob 5
    "B5_Row": "C73",
    "B5_Col": "C74",
    "B5_Area": "C75",

    # Blob 6
    "B6_Row": "C76",
    "B6_Col": "C77",
    "B6_Area": "C78",

    # Pattern
    "Pattern_Row": "C88",
    "Pattern_Col": "C89",
    "Pattern_Angle": "C90",
    "Pattern_Scale": "C91",
    "Pattern_Score": "C92",

    # Relative Row patterns
    "Rel_Row1": "C95",
    "Rel_Row2": "C96",
    "Rel_Row3": "C97",
    "Rel_Row4": "C98",
    "Rel_Row5": "C99",
    "Rel_Row6": "C100",

    # Relative Col patterns
    "Rel_Col1": "C102",
    "Rel_Col2": "C103",
    "Rel_Col3": "C104",
    "Rel_Col4": "C105",
    "Rel_Col5": "C106",
    "Rel_Col6": "C107",
}

# ==============================
# Connect Cognex
# ==============================

def connect():

    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    s.settimeout(5)

    print("Connecting...")
    s.connect((IP, PORT))


    # Welcome
    print(s.recv(1024).decode())


    # Username
    s.sendall(b"admin\r\n")
    time.sleep(1)

    print(s.recv(1024).decode())


    # Password empty
    s.sendall(b"\r\n")
    time.sleep(1)

    print(s.recv(1024).decode())


    print("Logged in")

    return s



# ==============================
# Read Cognex cell
# ==============================

def read_cell(s, cell):

    command = "GVC" + cell[1:]

    s.sendall(
        (command + "\r\n").encode()
    )

    time.sleep(0.15)

    response = s.recv(1024).decode()

    lines = response.splitlines()


    # Cognex answer:
    # 1
    # value

    if len(lines) >= 2:

        try:
            return float(lines[1])

        except:
            return None


    return None



# ==============================
# Collect data
# ==============================


s = connect()


filename = "GOOD_parts.csv"


with open(filename, "w", newline="") as file:


    writer = csv.writer(file)


    header = [
        "Image"
    ] + list(CELLS.keys())


    writer.writerow(header)



    number_of_images = 100


    for image in range(1, number_of_images + 1):


        row = [
            image
        ]


        values=[]


        for name, cell in CELLS.items():

            value = read_cell(
                s,
                cell
            )

            values.append(value)



        row += values


        writer.writerow(row)


        print(
            "Image",
            image,
            values
        )


        time.sleep(1)



s.close()


print("DONE")
print(filename)