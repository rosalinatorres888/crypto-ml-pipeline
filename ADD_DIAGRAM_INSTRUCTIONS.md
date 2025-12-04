# INSTRUCTIONS: Upload Your UML Diagram

## The README is ready and references: `images/crypto-ml-uml.png`

To complete the update, upload your UML class diagram:

### Option 1: Via GitHub Web Interface
1. Go to: https://github.com/rosalinatorres888/crypto-ml-pipeline
2. Navigate to (or create) the `images/` folder
3. Click "Add file" → "Upload files"
4. Upload your UML diagram as `crypto-ml-uml.png`
5. Commit

### Option 2: Via Terminal (if you have the image saved)
```bash
# Save your UML diagram to Desktop as crypto-ml-uml.png
# Then run:
cd ~/Documents/crypto-ml-pipeline
cp ~/Desktop/crypto-ml-uml.png images/
git add images/crypto-ml-uml.png
git commit -m "Add UML class diagram"
git push origin main
```

## What the Diagram Shows

Your UML diagram demonstrates:
- **Professional OOP design** with clear class hierarchies
- **Interface-based architecture** (MLModel interface)
- **Design patterns** (Strategy, Factory, Observer, Singleton)
- **Production thinking** (DatabaseManager with connection pooling)
- **Clean separation of concerns** (Airflow, Data, ML, Storage, UI)

This is EXACTLY what separates junior from senior engineers!
