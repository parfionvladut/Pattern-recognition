import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import seaborn as sns




image_size = (180, 180)
batch_size = 32

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "C:/Users/jacso/Desktop/PetImages",
    validation_split=0.2,
    subset="training",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
)
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "C:/Users/jacso/Desktop/PetImages",
    validation_split=0.2,
    subset="validation",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
)



data_augmentation = keras.Sequential(
    [
        layers.experimental.preprocessing.RandomFlip("horizontal"),
        layers.experimental.preprocessing.RandomRotation(0.1),
    ]
)

train_ds = train_ds.prefetch(buffer_size=32)
val_ds = val_ds.prefetch(buffer_size=32) 

def make_model(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)
    
    # Image augmentation block
    x = data_augmentation(inputs)
    

    # Entry block
    x = layers.experimental.preprocessing.Rescaling(1.0 / 255)(x)
    x = layers.Conv2D(32, 3, strides=2, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.Conv2D(64, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    previous_block_activation = x  # Set aside residual

    for size in [128, 256, 512, 728]:
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)

        # Project residual
        residual = layers.Conv2D(size, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    x = layers.SeparableConv2D(1024, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.GlobalAveragePooling2D()(x)
    if num_classes == 2:
        activation = "sigmoid"
        units = 1
    else:
        activation = "softmax"
        units = num_classes

    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(units, activation=activation)(x)
    return keras.Model(inputs, outputs)


model = make_model(input_shape=image_size + (3,), num_classes=2)
#model.summary()
keras.utils.plot_model(model, show_shapes=True)




while True:        
     x = input("Would you like to train the algorithm?(y/n) \n Warning:the process will take more than 10 min ")
     if( x=="y" or x=="n"):
        break
model.load_weights("C:/Users/jacso/Desktop/Lab/PatternRecognition/save_at_45.h5") 
   
if x=="y":
    epochs = 50

    callbacks = [
    keras.callbacks.ModelCheckpoint("save_at_{epoch}.h5"),
]
    model.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss="binary_crossentropy",
    metrics=["accuracy"],
)
    model.fit(
    train_ds, epochs=epochs, callbacks=callbacks, validation_data=val_ds,
)



img = keras.preprocessing.image.load_img(
    "C:/Users/jacso/Desktop/PetImages/Cat/6779.jpg", target_size=image_size
)
plt.imshow(img)
plt.axis("off")
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Create batch axis

predictions = model.predict(img_array)

score = predictions[0]

if 100 * (1 - score)>50:
    print(
    "This is a cat"
    
)
else:
    print("This is a dog")
model.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss="binary_crossentropy",
    metrics=["accuracy"],
)
model.evaluate(val_ds)




y_pred = model.predict(val_ds)

predicted_categories = tf.argmax(y_pred, axis=-1)
true_categories = tf.concat([y for x, y in val_ds], axis=0)

print(true_categories)

print(predicted_categories)

sns.heatmap(confusion_matrix(predicted_categories, true_categories),annot=True ,fmt="d")

target_names = ['Cats', 'Dogs']
print(classification_report(true_categories, predicted_categories, target_names=target_names))






                                


