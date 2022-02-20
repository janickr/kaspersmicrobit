from kaspersmicrobit.services.io_pin import Pin, PinValue, PwmControlData, PinIO, PinAD, PinConfiguration, PinIOConfiguration, PinADConfiguration


class TestPinValue:
    def test_to_bytes(self):
        value = PinValue(Pin.P3, 255)
        assert value.to_bytes() == bytearray.fromhex("03 3F")

    def test_from_bytes(self):
        value = PinValue.from_bytes(bytearray.fromhex("10 0A"))
        assert value == PinValue(Pin.P16, 40)

    def test_compression_from_10_to_8_bits_loses_resolution(self):
        value = PinValue.from_bytes(PinValue(Pin.P3, 255).to_bytes())

        assert value.value == 252


class TestPinIOConfiguration:
    def test_default_is_all_output(self):
        pins = PinIOConfiguration()
        assert pins[Pin.P0:] == [PinIO.OUTPUT] * PinConfiguration.NUMBER_OF_PINS

    def test_change_one_pin_config(self):
        pins = PinIOConfiguration()
        pins[Pin.P5] = PinIO.INPUT
        expected = [PinIO.OUTPUT] * PinConfiguration.NUMBER_OF_PINS
        expected[5] = PinIO.INPUT
        assert pins[Pin.P0:] == expected

    def test_from_bytes(self):
        pins = PinIOConfiguration.from_bytes(bytearray.fromhex("21 84 00 00"))
        expected = [PinIO.OUTPUT] * PinConfiguration.NUMBER_OF_PINS
        expected[0] = PinIO.INPUT
        expected[5] = PinIO.INPUT
        expected[10] = PinIO.INPUT
        expected[15] = PinIO.INPUT
        assert pins[Pin.P0:] == expected

    def test_to_bytes(self):
        pins = PinIOConfiguration()
        pins[Pin.P0] = PinIO.INPUT
        pins[Pin.P5] = PinIO.INPUT
        pins[Pin.P10] = PinIO.INPUT
        pins[Pin.P15] = PinIO.INPUT
        assert pins.to_bytes() == bytearray.fromhex("21 84 00 00")


class TestPinADConfiguration:
    def test_default_is_all_digital(self):
        pins = PinADConfiguration()
        assert pins[Pin.P0:] == [PinAD.DIGITAL] * PinConfiguration.NUMBER_OF_PINS

    def test_change_one_pin_config(self):
        pins = PinADConfiguration()
        pins[Pin.P5] = PinAD.ANALOG
        expected = [PinAD.DIGITAL] * PinConfiguration.NUMBER_OF_PINS
        expected[5] = PinAD.ANALOG
        assert pins[Pin.P0:] == expected

    def test_from_bytes(self):
        pins = PinADConfiguration.from_bytes(bytearray.fromhex("21 84 00 00"))
        expected = [PinAD.DIGITAL] * PinConfiguration.NUMBER_OF_PINS
        expected[0] = PinAD.ANALOG
        expected[5] = PinAD.ANALOG
        expected[10] = PinAD.ANALOG
        expected[15] = PinAD.ANALOG
        assert pins[Pin.P0:] == expected

    def test_to_bytes(self):
        pins = PinADConfiguration()
        pins[Pin.P0] = PinAD.ANALOG
        pins[Pin.P5] = PinAD.ANALOG
        pins[Pin.P10] = PinAD.ANALOG
        pins[Pin.P15] = PinAD.ANALOG
        assert pins.to_bytes() == bytearray.fromhex("21 84 00 00")


class TestPwmControlData:
    def test_to_bytes(self):
        value = PwmControlData(Pin.P6, 1024, 1234567)
        assert value.to_bytes() == bytearray.fromhex("06 00 04 87 D6 12 00")

    def test_from_bytes(self):
        value = PwmControlData.from_bytes(bytearray.fromhex("0E 0A 00 87 D6 12 00"))
        assert value == PwmControlData(Pin.P14, 10, 1234567)
