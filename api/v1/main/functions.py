def generate_serializer_errors(args):
    message = ""
    for key, values in args.items():
        error_message = ""
        for value in values:
            if key == 'non_field_errors' and 'invalid_campus' in value:
                error_message = "Invalid campus."
                return error_message
            else:
                error_message += value + ","
        error_message = error_message[:-1]

        # message += "%s : %s | " %(key,error_message)
        message += f"{key} - {error_message} | "
    return message[:-3]