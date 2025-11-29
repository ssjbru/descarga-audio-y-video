"""
Generador de certificados SSL auto-firmados para desarrollo local
NOTA: Estos certificados solo sirven para desarrollo/pruebas locales
Para producción, usa certificados reales de Let's Encrypt
"""
import os
from datetime import datetime, timedelta, timezone
import ipaddress

try:
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
except ImportError:
    print("❌ Error: Se necesita instalar cryptography")
    print("Ejecuta: pip install cryptography")
    exit(1)

def generate_self_signed_cert():
    """Genera un certificado SSL auto-firmado"""
    
    # Crear directorio ssl si no existe
    os.makedirs('ssl', exist_ok=True)
    
    # Generar clave privada
    print("🔐 Generando clave privada...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Guardar clave privada
    with open('ssl/key.pem', 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    print("✓ Clave privada guardada en ssl/key.pem")
    
    # Crear certificado
    print("📜 Generando certificado SSL...")
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Madrid"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Madrid"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Descargar de YT"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now(timezone.utc)
    ).not_valid_after(
        datetime.now(timezone.utc) + timedelta(days=365)  # Válido por 1 año
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("localhost"),
            x509.DNSName("127.0.0.1"),
            x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256(), default_backend())
    
    # Guardar certificado
    with open('ssl/cert.pem', 'wb') as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    print("✓ Certificado guardado en ssl/cert.pem")
    
    print("\n✅ Certificados SSL generados exitosamente!")
    print("\n⚠ IMPORTANTE:")
    print("  • Estos certificados son AUTO-FIRMADOS (solo para desarrollo)")
    print("  • Tu navegador mostrará una advertencia de seguridad")
    print("  • Para aceptarla, haz clic en 'Avanzado' > 'Continuar a localhost'")
    print("\n📌 Para producción con dominio real:")
    print("  1. Compra un dominio (Namecheap, GoDaddy, etc.)")
    print("  2. Configura DNS apuntando a tu servidor")
    print("  3. Usa Certbot para obtener certificados reales de Let's Encrypt:")
    print("     sudo certbot certonly --standalone -d tudominio.com")
    print("\n🚀 Para iniciar el servidor HTTPS:")
    print("  python app_secure.py")

if __name__ == '__main__':
    generate_self_signed_cert()
