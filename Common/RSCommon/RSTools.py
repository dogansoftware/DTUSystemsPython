
class RSTools:
    @staticmethod
    def calc_cs(src, src_offset, len):
        total = 0
        for i in range(src_offset, src_offset + len):
            total += src[i]
        return total & 0xFF  # Ensure the result is a byte value

    @staticmethod
    def ByteArrayToHexStr(byte_array, start, length):
        # Convert byte array to hex string
        return ''.join(f'{byte:x}' for byte in byte_array[start:start+length])
    @staticmethod
    def hex_str_to_byte_array(str_hex):
        str_hex = str_hex.strip().replace(" ", "")
        if len(str_hex) % 2 != 0:
            str_hex += "0"
        return bytes.fromhex(str_hex)