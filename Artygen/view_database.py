import sqlite3
import os

# Chemin vers la base de données
db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

def format_table(headers, rows):
    """Format data as a simple ASCII table"""
    if not rows:
        return "Aucune donnée"
    
    # Calculate column widths
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Create separator line
    separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    
    # Create header
    header_line = "| " + " | ".join(str(h).ljust(w) for h, w in zip(headers, col_widths)) + " |"
    
    # Create rows
    table_rows = []
    for row in rows:
        row_line = "| " + " | ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths)) + " |"
        table_rows.append(row_line)
    
    # Combine all parts
    result = [separator, header_line, separator]
    result.extend(table_rows)
    result.append(separator)
    
    return "\n".join(result)

def view_database():
    """Affiche toutes les tables et leur contenu de la base de données"""
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Récupérer la liste de toutes les tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = cursor.fetchall()
    
    print("=" * 100)
    print(f"📊 BASE DE DONNÉES: db.sqlite3")
    print(f"📁 Chemin: {db_path}")
    print(f"📋 Nombre de tables: {len(tables)}")
    print("=" * 100)
    
    # Pour chaque table, afficher son contenu
    for table_tuple in tables:
        table_name = table_tuple[0]
        
        # Ignorer les tables système
        if table_name.startswith('sqlite_'):
            continue
        
        print(f"\n\n{'=' * 100}")
        print(f"📌 TABLE: {table_name}")
        print('=' * 100)
        
        # Récupérer les informations sur les colonnes
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns_info = cursor.fetchall()
        column_names = [col[1] for col in columns_info]
        
        # Compter le nombre de lignes
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cursor.fetchone()[0]
        
        print(f"📊 Nombre de colonnes: {len(column_names)}")
        print(f"📈 Nombre de lignes: {row_count}")
        print(f"🔑 Colonnes: {', '.join(column_names)}")
        
        # Récupérer toutes les données
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100;")  # Limite à 100 lignes
        rows = cursor.fetchall()
        
        if rows:
            # Tronquer les valeurs trop longues pour l'affichage
            truncated_rows = []
            for row in rows:
                truncated_row = []
                for value in row:
                    if isinstance(value, str) and len(value) > 50:
                        truncated_row.append(value[:47] + '...')
                    else:
                        truncated_row.append(value)
                truncated_rows.append(truncated_row)
            
            # Afficher le tableau
            print("\n" + format_table(column_names, truncated_rows))
            
            if row_count > 100:
                print(f"\n⚠️ Affichage limité aux 100 premières lignes (total: {row_count} lignes)")
        else:
            print("\n❌ Table vide")
    
    # Fermer la connexion
    conn.close()
    
    print("\n" + "=" * 100)
    print("✅ Analyse terminée!")
    print("=" * 100)

def view_specific_tables(table_names):
    """Affiche le contenu de tables spécifiques"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for table_name in table_names:
        print(f"\n\n{'=' * 100}")
        print(f"📌 TABLE: {table_name}")
        print('=' * 100)
        
        try:
            # Récupérer les informations sur les colonnes
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]
            
            # Récupérer toutes les données
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            
            print(f"📊 Nombre de lignes: {len(rows)}")
            
            if rows:
                # Afficher le tableau
                print("\n" + format_table(column_names, rows))
            else:
                print("\n❌ Table vide")
        
        except sqlite3.Error as e:
            print(f"❌ Erreur: {e}")
    
    conn.close()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # Si des noms de tables sont fournis en arguments
        view_specific_tables(sys.argv[1:])
    else:
        # Sinon, afficher toutes les tables
        view_database()
