
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