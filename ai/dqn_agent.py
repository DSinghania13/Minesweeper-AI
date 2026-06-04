import random
import numpy as np
import tensorflow as tf
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, Add, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from collections import deque


class DQNAgent:

    def __init__(self, state_shape, action_size, pretrained_model_path=None):
        self.state_shape = state_shape
        self.action_size = action_size
        self.memory = deque(maxlen=2000)

        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.0001

        self.model = self._build_model(pretrained_model_path)
        self.target_model = self._build_model(pretrained_model_path)
        self.update_target_model()

    def _build_model(self, pretrained_model_path):

        def res_block(x, filters):
            fx = Conv2D(filters, (3, 3), padding='same')(x)
            fx = BatchNormalization()(fx)
            fx = Activation('relu')(fx)
            fx = Conv2D(filters, (3, 3), padding='same')(fx)
            fx = BatchNormalization()(fx)
            out = Add()([x, fx])
            out = Activation('relu')(out)
            return out

        inputs = Input(shape=self.state_shape)
        x = Conv2D(128, (3, 3), padding='same')(inputs)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)

        x = res_block(x, 128)
        x = res_block(x, 128)
        x = res_block(x, 128)
        x = res_block(x, 128)

        x = Flatten()(x)
        x = Dense(512, activation='relu')(x)
        outputs = Dense(self.action_size, activation='linear')(x)

        model = Model(inputs=inputs, outputs=outputs)

        if pretrained_model_path:
            print(f"Loading pre-trained weights from {pretrained_model_path}")
            temp_model = tf.keras.models.load_model(
                pretrained_model_path,
                custom_objects={'mean_iou': lambda y_true, y_pred: 0.0}
            )
            for layer, temp_layer in zip(model.layers[:-3], temp_model.layers[:-1]):
                layer.set_weights(temp_layer.get_weights())

        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)

        act_values = self.model.predict(state, verbose=0)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return

        minibatch = random.sample(self.memory, batch_size)

        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.target_model.predict(next_state, verbose=0)[0]))

            target_f = self.model.predict(state, verbose=0)
            target_f[0][action] = target

            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay