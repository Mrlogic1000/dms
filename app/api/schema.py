from marshmallow import Schema, fields,validate,validates,ValidationError
import re



status = ['Active','Inactive','In Repair','Retired','Store']
device_type = ['Router','Switch','AP','CCTV','Computer','Other','NVR','DVR','Other']
manufacurs = ['Mikrotik','CISCO','Access Point','TP-Link','ASUS','Netgear'
           'CCTV','Computer','Other','Huawei','Juniper','D-Link','Linksys',
           'Google Nest','DrayTek','Eero','Hikvision','Axis Communications',
           'Dahua-Technology','Hanwha Vision','Bosch','Motorola','Panasonic',
           'Avigilon','HoneWell','MOBOTIX','VIVOTEK','IDIS','Ruckus',
           'Fortinet','Extreme','Aruba','Alcatel-Lucent','Cambium','Other'
           ]



class DeviceSchema(Schema):
    name = fields.Str(required=True)
    location = fields.Str(required=True)
    ip = fields.Str(required=True)
    model = fields.Str()
    mac = fields.Str(required=True)
    sn = fields.Str(required=True)
    purchase_date = fields.Str()
    status = fields.Str(required=True,validate=validate.OneOf(status))
    create_at = fields.Date()
    device_type = fields.Str(required=True,validate=validate.OneOf(device_type))
    manufacture = fields.Str(required=True,validate=validate.OneOf(manufacurs))
    user_id = fields.Integer(required=True)
    @validates('mac')
    def validate_mac_address(self,value,data_key):
        """
        Validates if a given string is a valid MAC address.
        Supports formats with hyphens, colons, and dots.
        """
        # Regex for MAC addresses with hyphens or colons
        pattern_colon_hyphen = r"^([0-9a-fA-F]{2}(?:[-:]|$)){6}$"
        # Regex for MAC addresses with dots
        pattern_dot = r"^[0-9a-fA-F]{4}(?:\.|$){3}$"

        if re.match(pattern_colon_hyphen, value.lower()):
            return True
        elif re.match(pattern_dot, value.lower()):
            return True
        else:
            raise ValidationError("The Mac Address is incorrect. Put correct format")

