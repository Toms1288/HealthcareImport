db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

// Création d'utilisateur d'application avec des permissions 
db.createUser({
    user: process.env.MONGO_APP_USERNAME,
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
    ],
    mechanisms: ["SCRAM-SHA-256"]  // Utilise SHA-256 pour le hachage
});
// Création de la collection avec validation de schéma
db.createCollection(process.env.COLLECTION, {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: [
            "patient_id",
            "name",
            "age",
            "gender",
            "blood_type",
            "medical_condition",
            "date_of_admission",
            "doctor",
            "hospital",
            "insurance_provider",
            "billing_amount",
            "room_number",
            "admission_type",
            "discharge_date",
            "medication",
            "test_results"
         ],
         properties: {
            patient_id: {
               bsonType: "int",
               description: "Unique identifier for each patient."
            },
            name: {
               bsonType: "string",
               description: "Patient's name must be a string."
            },
            age: {
               bsonType: "int",
               minimum: 0,
               maximum: 150,
               description: "Age must be an integer between 0 and 150."
            },
            gender: {
               bsonType: "string",
               enum: ["Male", "Female", "Other"],
               description: "Gender must be 'Male', 'Female', or 'Other'."
            },
            blood_type: {
               bsonType: "string",
               enum: ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
               description: "Blood type must be a valid blood type."
            },
            medical_condition: {
               bsonType: "string",
               description: "Medical condition must be a string."
            },
            date_of_admission: {
               bsonType: "Date",
               description: "Must be a date"
            },
            doctor: {
               bsonType: "string",
               description: "Doctor's name must be a string."
            },
            hospital: {
               bsonType: "string",
               description: "Hospital name must be a string."
            },
            insurance_provider: {
               bsonType: "string",
               description: "Insurance provider must be a string."
            },
            billing_amount: {
               bsonType: "double",
               minimum: 0,
               description: "Billing amount must be a non-negative number."
            },
            room_number: {
               bsonType: "int",
               minimum: 1,
               description: "Room number must be a positive integer."
            },
            admission_type: {
               bsonType: "string",
               enum: ["Elective", "Urgent", "Emergency"],
               description: "Admission type must be one of the specified values."
            },
            discharge_date: {
               bsonType: "Date",
               description: "Must be a date"
            },
            medication: {
               bsonType: "string",
               description: "Medication details must be a string."
            },
            test_results: {
               bsonType: "string",
               enum: ["Normal", "Abnormal", "Inconclusive"],
               description: "Test results must be one of the specified values."
            }
         }
      }
   }
});
