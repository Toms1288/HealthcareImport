db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

// Création d'utilisateur d'application avec des permissions 
db.createUser({
    user: process.env.MONGO_APP_USER,
    pwd: process.env.MONGO_APP_PASSWORD,
    roles: [
        {
            role: "readWrite",
            db: process.env.MONGO_INITDB_DATABASE
        },
        {
            role: "dbAdmin",
            db: process.env.MONGO_INITDB_DATABASE
        },
        {
            role: "readWrite",
            db: "test_database"
        },
        {
            role: "dbAdmin",
            db: "test_database"
        }
    ],
    mechanisms: ["SCRAM-SHA-256"]  // Utilise SHA-256 pour le hachage
});

// Collection Patient
db.createCollection("patient", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["name", "age", "gender", "bloodType"],
            properties: {
                name: {
                bsonType: "string",
                description: "Nom du patient"
                },
                age: {
                bsonType: "number",
                description: "Âge du patient"
                },
                gender: {
                bsonType: "string",
                description: "Genre du patient"
                },
                bloodType: {
                bsonType: "string",
                description: "Groupe sanguin"
                }
            }
        }
    }
});
  
// Collection Medical
db.createCollection("medical", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["patientId", "condition", "medication", "testResults", "doctor"],
            properties: {
                patientId: {
                bsonType: "objectId",
                description: "Référence au patient"
                },
                condition: {
                bsonType: "string",
                description: "État médical"
                },
                medication: {
                bsonType: "string",
                description: "Médicaments"
                },
                testResults: {
                bsonType: "string",
                description: "Résultats des tests"
                },
                doctor: {
                bsonType: "string",
                description: "Nom du docteur"
                }
            }
        }
    }
});

// Collection Admission
db.createCollection("admission", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["patientId", "dateOfAdmission", "hospital", "roomNumber", "admissionType"],
            properties: {
                patientId: {
                bsonType: "objectId",
                description: "Référence au patient"
                },
                dateOfAdmission: {
                bsonType: "date",
                description: "Date d'admission"
                },
                dischargeDate: {
                bsonType: "date",
                description: "Date de sortie"
                },
                admissionType: {
                bsonType: "string",
                description: "Type d'admission "
                },
                roomNumber: {
                bsonType: "number",
                description: "Numéro de chambre"
                },
                hospital: {
                bsonType: "string",
                description: "Nom de l'hôpital"
                }
            }
        }
    }
})

// Collection Billing
db.createCollection("billing", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["patientId", "insuranceProvider", "amount"],
            properties: {
                patientId: {
                bsonType: "objectId",
                description: "Référence au patient"
                },
                insuranceProvider: {
                bsonType: "string",
                description: "Fournisseur d'assurance"
                },
                amount: {
                bsonType: "decimal",
                description: "Montant de la facturation"
                }
            }
        }
    }
})


// Création des autres index
db.patients.createIndex({ "name": 1 })
db.medical.createIndex({ "patientId": 1 })
db.admission.createIndex({ 
    "patientId": 1,
    "dateOfAdmission": 1
 })
db.billing.createIndex({ "patientId": 1 })