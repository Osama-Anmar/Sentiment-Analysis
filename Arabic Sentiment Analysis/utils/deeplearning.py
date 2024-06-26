import tensorflow as tf
import keras
from keras.layers import *
from tensorflow import *
from keras.preprocessing import *
import matplotlib.pyplot as plt
from keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint

def callbacks_ ():
    """create callback functions for model training

    Args:
        name (string): name using for model checkpoint file

    Returns:
        tuple: A tuple containing three callbacks:
            - ReduceLROnPlateau: Reduces learning rate when validation loss plateaus
            - EarlyStopping: Stops training when validation loss stops improving
            - ModelCheckpoint: Saves the best model weights based on validation loss
    """    ""
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.001)
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True,)

    return reduce_lr, early_stop

def lstm_(vocab_size, embedding_dim, max_length, units1, units2, units3, units4, dropout1, dropout2, dropout3, dropout4,  embeddings_matrix):
            """
        creates and returns a sequential LSTM model for sentiment analysis

        Args:
            vocab_size (integer): Size of the vocabulary (number of unique words).
            embedding_dim (integer): dimensionality of word embeddings
            units1 (integer): number of units in the first LSTM layer
            dropout1 (float): dropout rate for the first LSTM layer (0.0 to disable)
            units2 (integer): number of units in the second LSTM layer
            dropout2 (float): dropout rate for the second LSTM layer (0.0 to disable)
            units3 (integer): number of units in the dense layer before the output layer
            dropout3 (float): dropout rate for the dense layer (0.0 to disable)
            embeddings_matrix (np.ndarray): pre-trained word embedding matrix

        Returns:
            keras.Model: the compiled LSTM model
        """   
            model = keras.Sequential([
                Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length,  embeddings_initializer=keras.initializers.Constant(embeddings_matrix), trainable = True),
                LSTM(units=units1, dropout=dropout1, return_sequences=True, kernel_initializer=tf.keras.initializers.random_normal(seed=1), kernel_regularizer=keras.regularizers.L2(l2=0.001)),
                LSTM(units=units2, dropout=dropout2, return_sequences=True, kernel_initializer=tf.keras.initializers.random_normal(seed=1), kernel_regularizer=keras.regularizers.L2(l2=0.001)),
                LSTM(units=units3, dropout=dropout3, return_sequences=False, kernel_initializer=tf.keras.initializers.random_normal(seed=1), kernel_regularizer=keras.regularizers.L2(l2=0.001)),
                Dense(units4, activation= 'tanh', kernel_initializer=tf.keras.initializers.random_normal(seed=1), kernel_regularizer=keras.regularizers.L2(l2=0.001)),
                Dropout(dropout4),
                Dense(1, activation= 'sigmoid', kernel_initializer=tf.keras.initializers.random_normal(seed=1))
                ])     
            return model  

def gru_(vocab_size, embedding_dim, max_length, units1, dropout1, units2, dropout2, units3,  embeddings_matrix):
            """
                creates and returns a sequential GRU model for sentiment analysis

                Args:
                    vocab_size (integer): size of the vocabulary (number of unique words)
                    embedding_dim (integer): dimensionality of word embeddings
                    units1 (integer): number of units in the first GRU layer
                    dropout1 (float): dropout rate for the first GRU layer (0.0 to disable)
                    units2 (integer): number of units in the second GRU layer
                    dropout2 (float): dropout rate for the second GRU layer (0.0 to disable)
                    units3 (integer): number of units in the dense layer before the output layer
                    dropout3 (float): dropout rate for the dense layer (0.0 to disable)
                    embeddings_matrix (np.ndarray): pre-trained word embedding matrix

                Returns:
                    keras.Model: the compiled GRU model
             """
            model = tf.keras.Sequential([
                Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length,  embeddings_initializer=keras.initializers.Constant(embeddings_matrix), trainable = True),
                GRU(units=units1, dropout=dropout1, return_sequences=True, kernel_initializer=tf.keras.initializers.random_normal(seed=1), kernel_regularizer=keras.regularizers.L2(l2=0.001)),
                GRU(units=units2, dropout=dropout2, return_sequences=False,kernel_initializer=tf.keras.initializers.random_normal(seed=1), kernel_regularizer=keras.regularizers.L2(l2=0.001)),
                Dense(units=units3, activation= 'tanh', kernel_initializer=tf.keras.initializers.random_normal(seed=1), kernel_regularizer=keras.regularizers.L2(l2=0.001)),
                Dense(1, activation= 'sigmoid', kernel_initializer=tf.keras.initializers.random_normal(seed=1))
                ])     
            return model


def bidirectional_lstm(vocab_size, embedding_dim, max_length, units1, dropout1, units2, dropout2, units3, dropout3,  embeddings_matrix):
            """
                creates and returns a sequential bidirectional LSTM model for sentiment analysis

                Args:
                    vocab_size (integer): size of the vocabulary (number of unique words)
                    embedding_dim (integer): dimensionality of word embeddings
                    units1 (integer): number of units in the bidirectional LSTM layer
                    dropout1 (float): dropout rate for the bidirectional LSTM layer (0.0 to disable)
                    embeddings_matrix (np.ndarray): pre-trained word embedding matrix

                Returns:
                    keras.Model: the compiled bidirectional LSTM model.
            """
            model = keras.Sequential([
                Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length,  embeddings_initializer=keras.initializers.Constant(embeddings_matrix), trainable = True),
                Bidirectional(LSTM(units=units1, dropout=dropout1, return_sequences=True, kernel_initializer=tf.keras.initializers.random_normal(seed=1), kernel_regularizer=keras.regularizers.L2(l2=0.001))),
                Bidirectional(LSTM(units=units2, dropout=dropout2, return_sequences=False, kernel_initializer=tf.keras.initializers.random_normal(seed=1), kernel_regularizer=keras.regularizers.L2(l2=0.001))),
                Dense(units=units3, activation= 'tanh', kernel_initializer=tf.keras.initializers.random_normal(seed=1), kernel_regularizer=keras.regularizers.L2(l2=0.001)),
                Dropout(dropout3),
                Dense(1, activation= 'sigmoid', kernel_initializer=tf.keras.initializers.random_normal(seed=1))
                ])     
            return model  


def model_compile(model) :
        """
            compiles a provided Keras model with a common configuration suitable for sentiment analysis tasks

            Args:
                model (keras.Model): the Keras model to be compiled

            Returns:
                keras.Model: the compiled Keras model
    """
        return model.compile(optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=0.0001),
                            loss=tf.keras.losses.BinaryCrossentropy(),
                            metrics= ['accuracy'])
    
def model_fit(model, X_train, y_train, epochs, X_test, y_test, batch_size):       
        """
            fits a Keras model on training data with validation and early stopping.

        Args:
            model (keras.Model): the Keras model to be trained
            X_train (np.ndarray): training data features
            y_train (np.ndarray): training data labels
            epochs (int): number of training epochs
            X_test (np.ndarray): validation data features
            y_test (np.ndarray): validation data labels
            batch_size (int): batch size for training
            class_weights (dict, optional): dictionary of class weights for imbalanced datasets. Defaults to None
            name (string): name to be used for model checkpoint files

        Returns:
            keras.callbacks.History: Training history object containing performance metrics.
        """
        reduce_lr, early_stop = callbacks_()
        history = model.fit(X_train, y_train,
                    epochs=epochs,
                    validation_data=(X_test, y_test),
                    batch_size=batch_size,
                    callbacks=[early_stop, reduce_lr])
        return history
    

