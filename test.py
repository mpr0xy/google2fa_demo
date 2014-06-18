import googauth

secret_key = googauth.generate_secret_key()

print secret_key


print googauth.verify_time_based('GJJPCB2WZJAOX37Y', '345248', 6)



print googauth.get_barcode_url('user', 'domain.com', secret_key)