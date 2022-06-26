from paystackapi.charge import Charge
response = Charge.start_charge(
            email="CUS_je02lbimlqixzax",
            amount=42000,
            metadata={
                "custom_fields": [
                    {
                        "value":"makurdi",
                        "display_name": "Donation for",
                        "variable_name": "donation_for"
                    },
                ],
            },
            bank={
                "code":"057",
                "account_number":"0000000000"
            },
            birthday="1995-12-23"
        )

from paystackapi.charge import Charge
response = Charge.submit_pin(
            pin="0987",
            reference="5bwib5v6anhe9xa",
        )

from paystackapi.charge import Charge
response = Charge.submit_otp(
            otp="0987",
            reference="5bwib5v6anhe9xa",
        )

from paystackapi.charge import Charge
response = Charge.check_pending(
            reference="5bwib5v6anhe9xa",
        )