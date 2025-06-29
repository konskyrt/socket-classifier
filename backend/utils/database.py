import sqlite3
import json
import os

class Database:
    def __init__(self, db_path='data/outlets.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    def initialize(self):
        """Initialize database with tables and sample data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create outlets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS outlets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                outlet_type TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                country_code TEXT,
                voltage TEXT,
                current_rating TEXT,
                frequency TEXT,
                plug_type TEXT,
                natural_image_url TEXT,
                product_image_url TEXT
            )
        ''')
        
        # Create outlet_specifications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS outlet_specifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                outlet_type TEXT NOT NULL,
                width REAL,
                height REAL,
                depth REAL,
                hole_diameter REAL,
                hole_spacing REAL,
                mounting_screws TEXT,
                geometry_data TEXT
            )
        ''')
        
        # Insert sample data
        self._insert_sample_data(cursor)
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    
    def _insert_sample_data(self, cursor):
        """Insert sample electrical socket data"""
        outlets_data = [
            ('NEMA_5-15R', 'NEMA 5-15R Standard Socket', 'Standard US household wall socket', 'US', '120V', '15A', '60Hz', 'Type A/B', 
             'https://via.placeholder.com/400x300/ffffff/333333?text=US+Socket+Installation', 
             'https://via.placeholder.com/400x300/f8f9fa/495057?text=NEMA+5-15R+Socket'),
            ('BS_1363', 'BS 1363 UK Socket', 'Standard UK three-pin wall socket', 'UK', '230V', '13A', '50Hz', 'Type G', 
             'https://via.placeholder.com/400x300/ffffff/333333?text=UK+Socket+Installation', 
             'https://via.placeholder.com/400x300/f8f9fa/495057?text=BS+1363+Socket'),
            ('CEE_7/4', 'CEE 7/4 Schuko Socket', 'European Schuko wall socket', 'EU', '230V', '16A', '50Hz', 'Type F', 
             'https://via.placeholder.com/400x300/ffffff/333333?text=EU+Socket+Installation', 
             'https://via.placeholder.com/400x300/f8f9fa/495057?text=Schuko+Socket'),
            ('AS_3112', 'AS 3112 Australian Socket', 'Standard Australian wall socket', 'AU', '230V', '10A', '50Hz', 'Type I', 
             'https://via.placeholder.com/400x300/ffffff/333333?text=AU+Socket+Installation', 
             'https://via.placeholder.com/400x300/f8f9fa/495057?text=AS+3112+Socket'),
            ('JIS_C_8303', 'JIS C 8303 Japanese Socket', 'Standard Japanese wall socket', 'JP', '100V', '15A', '50/60Hz', 'Type A/B', 
             'https://via.placeholder.com/400x300/ffffff/333333?text=JP+Socket+Installation', 
             'https://via.placeholder.com/400x300/f8f9fa/495057?text=JIS+C+8303+Socket'),
            ('GFCI', 'GFCI Protected Socket', 'US GFCI safety wall socket', 'US', '120V', '15A', '60Hz', 'Type A/B', 
             'https://via.placeholder.com/400x300/ffffff/333333?text=GFCI+Socket+Installation', 
             'https://via.placeholder.com/400x300/f8f9fa/495057?text=GFCI+Socket'),
            ('USB_A', 'USB-A Socket', 'USB Type-A charging wall socket', 'Universal', '5V', '2.4A', 'DC', 'USB-A', 
             'https://via.placeholder.com/400x300/ffffff/333333?text=USB-A+Socket+Installation', 
             'https://via.placeholder.com/400x300/f8f9fa/495057?text=USB-A+Socket'),
            ('USB_C', 'USB-C Socket', 'USB Type-C charging wall socket', 'Universal', '5V', '3A', 'DC', 'USB-C', 
             'https://via.placeholder.com/400x300/ffffff/333333?text=USB-C+Socket+Installation', 
             'https://via.placeholder.com/400x300/f8f9fa/495057?text=USB-C+Socket')
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO outlets 
            (outlet_type, name, description, country_code, voltage, current_rating, frequency, plug_type, natural_image_url, product_image_url) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', outlets_data)
        
        # Insert specifications data
        specs_data = [
            ('NEMA_5-15R', 114.3, 69.9, 44.5, 6.35, 12.7, 'M3.5x32mm', '{"holes": [{"x": 0, "y": 10, "diameter": 6.35}, {"x": 0, "y": -10, "diameter": 6.35}]}'),
            ('BS_1363', 86, 86, 47, 8, 22, 'M4x35mm', '{"holes": [{"x": -11, "y": 11, "diameter": 8}, {"x": 11, "y": 11, "diameter": 8}]}'),
            ('CEE_7/4', 84, 84, 55, 4.8, 19, 'M4x40mm', '{"holes": [{"x": -9.5, "y": 0, "diameter": 4.8}, {"x": 9.5, "y": 0, "diameter": 4.8}]}'),
            ('AS_3112', 80, 110, 55, 8, 32, 'M4x40mm', '{"holes": [{"x": 0, "y": 16, "diameter": 8}, {"x": -16, "y": -16, "diameter": 8}, {"x": 16, "y": -16, "diameter": 8}]}'),
            ('JIS_C_8303', 77, 52, 42, 6.35, 12.7, 'M3.5x32mm', '{"holes": [{"x": 0, "y": 6.35, "diameter": 6.35}, {"x": 0, "y": -6.35, "diameter": 6.35}]}'),
            ('GFCI', 114.3, 95, 55, 6.35, 12.7, 'M3.5x40mm', '{"holes": [{"x": 0, "y": 10, "diameter": 6.35}, {"x": 0, "y": -10, "diameter": 6.35}], "gfci": true}'),
            ('USB_A', 69, 15, 12, None, None, 'M2.5x20mm', '{"connector": {"width": 12, "height": 4.5, "depth": 14}}'),
            ('USB_C', 69, 15, 12, None, None, 'M2.5x20mm', '{"connector": {"width": 8.5, "height": 2.6, "depth": 14}}')
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO outlet_specifications 
            (outlet_type, width, height, depth, hole_diameter, hole_spacing, mounting_screws, geometry_data) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', specs_data)
    
    def get_product_by_type(self, outlet_type):
        """Get product information by socket type"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM outlets WHERE outlet_type = ?
        ''', (outlet_type,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'outlet_type': result[1],
                'name': result[2],
                'description': result[3],
                'country_code': result[4],
                'voltage': result[5],
                'current_rating': result[6],
                'frequency': result[7],
                'plug_type': result[8],
                'natural_image_url': result[9],
                'product_image_url': result[10]
            }
        return None
    
    def get_product_specs(self, outlet_type):
        """Get detailed specifications for socket type"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT os.*, o.name, o.description 
            FROM outlet_specifications os
            JOIN outlets o ON os.outlet_type = o.outlet_type
            WHERE os.outlet_type = ?
        ''', (outlet_type,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            geometry_data = json.loads(result[8]) if result[8] else {}
            return {
                'outlet_type': result[1],
                'dimensions': {
                    'width': result[2],
                    'height': result[3],
                    'depth': result[4]
                },
                'hole_diameter': result[5],
                'hole_spacing': result[6],
                'mounting_screws': result[7],
                'geometry_data': geometry_data,
                'name': result[9],
                'description': result[10]
            }
        return None
    
    def get_all_outlet_types(self):
        """Get all supported socket types"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT outlet_type, name FROM outlets ORDER BY name')
        results = cursor.fetchall()
        conn.close()
        
        return [{'type': row[0], 'name': row[1]} for row in results]
    
    def add_outlet_type(self, outlet_data, specs_data):
        """Add new socket type to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Insert outlet
            cursor.execute('''
                INSERT INTO outlets 
                (outlet_type, name, description, country_code, voltage, current_rating, frequency, plug_type) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', outlet_data)
            
            # Insert specifications
            cursor.execute('''
                INSERT INTO outlet_specifications 
                (outlet_type, width, height, depth, hole_diameter, hole_spacing, mounting_screws, geometry_data) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', specs_data)
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error adding socket type: {e}")
            return False
        finally:
            conn.close() 