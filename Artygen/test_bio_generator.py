"""
Test du générateur de bio IA
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artify.settings')
django.setup()

from accounts.bio_generator import get_bio_generator

print("="*70)
print("🧪 TEST DU GÉNÉRATEUR DE BIO IA")
print("="*70)

# Test 1: Artiste avec style et intérêts complets
print("\n📝 Test 1: Artiste Digital Art")
print("-" * 70)

bio_gen = get_bio_generator()

result1 = bio_gen.generate_bio(
    username="PixelMaster",
    first_name="Marie",
    last_name="Dubois",
    art_style="Art digital, Illustrations futuristes, Cyberpunk",
    art_interests="technologie, neon, science-fiction, personnages, mondes imaginaires",
    tone='professional'
)

if result1['success']:
    print("✅ Génération réussie!")
    print("\n📄 BIO GÉNÉRÉE:")
    print(result1['bio'])
else:
    print(f"❌ Erreur: {result1['error']}")

# Test 2: Photographe nature
print("\n" + "="*70)
print("\n📝 Test 2: Photographe Nature")
print("-" * 70)

result2 = bio_gen.generate_bio(
    username="NatureShots",
    first_name="Jean",
    last_name="Martin",
    art_style="Photographie de paysages, Macro photographie",
    art_interests="nature, montagnes, forêts, wildlife, lumière naturelle, saisons",
    tone='professional'
)

if result2['success']:
    print("✅ Génération réussie!")
    print("\n📄 BIO GÉNÉRÉE:")
    print(result2['bio'])
else:
    print(f"❌ Erreur: {result2['error']}")

# Test 3: Artiste débutant avec peu d'infos
print("\n" + "="*70)
print("\n📝 Test 3: Artiste Débutant")
print("-" * 70)

result3 = bio_gen.generate_bio(
    username="ArtLover123",
    first_name="Sophie",
    last_name="Leroux",
    art_style="Peinture",
    art_interests="couleurs, émotions",
    tone='casual'
)

if result3['success']:
    print("✅ Génération réussie!")
    print("\n📄 BIO GÉNÉRÉE:")
    print(result3['bio'])
else:
    print(f"❌ Erreur: {result3['error']}")

# Test 4: Ton créatif
print("\n" + "="*70)
print("\n📝 Test 4: Artiste avec ton créatif")
print("-" * 70)

result4 = bio_gen.generate_bio(
    username="AbstractDreamer",
    first_name="Lucas",
    last_name="Bernard",
    art_style="Art abstrait, Mixed media",
    art_interests="formes géométriques, textures, chaos contrôlé, équilibre",
    tone='creative'
)

if result4['success']:
    print("✅ Génération réussie!")
    print("\n📄 BIO GÉNÉRÉE:")
    print(result4['bio'])
else:
    print(f"❌ Erreur: {result4['error']}")

print("\n" + "="*70)
print("✅ TESTS TERMINÉS!")
print("="*70)
