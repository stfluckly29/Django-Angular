def send_push_notification(token, cert_file, key_file, use_sandbox):
    import time
    from apns import APNs, Frame, Payload
    import datetime
    d = datetime.datetime.utcnow()
    date_str = d.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    apns = APNs(use_sandbox=use_sandbox, cert_file=cert_file, key_file=key_file)

    payload = Payload(content_available=True, custom={'date': date_str})
    # payload = Payload(alert="Hello World!", sound="default")
    apns.gateway_server.send_notification(token, payload)