import osudb
import ast
import struct

with open("./osu!MapSync/scores.db", "rb") as f:
    with open("Exp.txt", "w") as i:
        for stuff in f:
            i.write(str(stuff))

parse = osudb.parse_score(r"./osu!MapSync/scores.db")
with open('./osu!MapSync/output.txt', 'w') as f:
    f.write(str(parse)) #[1:-1].split(',')

def serialize_type_exp(fobj, data_type):
    if data_type == "Boolean": ## False if 0x00 else True
        return struct.pack("<?", fobj)
    elif data_type == "Byte": ## 1 byte int
        return struct.pack("<s", fobj)
    elif data_type == "Double": ## 8 bytes floating point
        return struct.pack("<d", fobj)
    elif data_type == "Int": ## 4 bytes unsigned int
        return struct.pack("<I", fobj)
    elif data_type == "Long": ## 8 bytes unsigned int
        return struct.pack("<Q", fobj)
    elif data_type == "Short": ## 2 bytes unsigned int
        return struct.pack("<H", fobj)
    elif data_type == "Single": ## 4 bytes floating point
        return struct.pack("<f", fobj)
    elif data_type == "String": ## 0x00 or 0x0b - ULE128(n) - UTF-8(length=n)
        bb = fobj
        if bb == None:
            return None
        return fobj.encode("utf-8")
    else:
        raise NotImplementedError('parse_type(fobj, data_type): Unknown data type: "%s".' % data_type)

def serialize_types_exp(fobj, types):
    return [serialize_type_exp(fobj, i) for i in types]

score_data_types = ['Byte', 'Int', 'String', 'String', 'String', 'Short', 'Short', 'Short', 'Short', 'Short', 'Short', 'Int', 'Short', 'Boolean', 'Int', 'String', 'Long', 'Int', 'Long']

def serialize_scoredb_data(file_path):
    with open(file_path, "r") as fobj:
        with open("./new osu!.db/scores.db", "wb") as otp:
            otp.truncate(0)
            for i in fobj:
                fobj = ast.literal_eval(i)
            for i in range(2):
                otp.write((serialize_type_exp(fobj[i],'Int')))
            for maps in fobj[2]:
                for i in range(2):
                    if type(maps[i]) == str:
                        otp.write(b'\x0b '+serialize_type_exp(maps[i],'String'))
                    if type(maps[i]) == int:
                        otp.write(serialize_type_exp(maps[i],'Int'))
                for scores in maps[2]:
                    for idx, stats in enumerate(scores): 
                        if score_data_types[idx] == 'Byte':
                            print(score_data_types[idx],stats,"->",bytes(stats),":",serialize_type_exp(bytes(stats), score_data_types[idx]))
                            otp.write(serialize_type_exp(bytes(stats), score_data_types[idx]))
                        elif stats == None:
                            print(score_data_types[idx],"None :", str("b'\x00"))
                            otp.write(b'\x00')
                        elif score_data_types[idx] == 'String' and len(stats) == 32:
                            print(score_data_types[idx],stats,"->",b'\x0b '+serialize_type_exp(stats, score_data_types[idx]))
                            otp.write(b'\x0b '+serialize_type_exp(stats, score_data_types[idx]))
                        elif idx == 3:
                            print(score_data_types[idx],stats,"->",b'\x0b\x06'+serialize_type_exp(stats, score_data_types[idx]))
                            otp.write(b'\x0b\x06'+serialize_type_exp(stats, score_data_types[idx]))
                        else:
                            print(score_data_types[idx],stats,"->",serialize_type_exp(stats, score_data_types[idx]))    
                            otp.write(serialize_type_exp(stats, score_data_types[idx]))

serialize_scoredb_data('./osu!MapSync/output.txt')

with open("./osu!MapSync/output_func.db", "rb") as f:
    with open("output_func.txt", "w") as i:
        for stuff in f:
            i.write(str(stuff))
