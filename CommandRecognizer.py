from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tensorflow.python.ops import io_ops
import numpy as np
import soundfile as sf


from model.recognize_commands import RecognizeResult, RecognizeCommands
from CommandRecorder import recordCommandPyAudio

class Recognizer:
    def __init__(self):
        super().__init__()
        self.model_list = [
            "./model/e01/frozen_graph_e01.pb",
            "./model/e001/frozen_graph_e001.pb",
            "./model/e001_conv_leaky_relu/conv_leaky_relu_graph.pb",
            "./model/e01_light_weight/frozen_model_e01_light_weight.pb",
            "./model/e001_light_weight/frozen_graph_e001_light_weight.pb",
        ]

    def classifyCommand(self, command):
        commandClass = "silence"
        commands = self.recognize()
        if len(commands) > 0:
            commandClass = commands[0]
            print("Recognized Command: ", commandClass)
        return commandClass

    def load_graph(self, frozen_graph_filename):
        graph = tf.Graph()
        with graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(frozen_graph_filename, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        return graph
 
    def recognize(self):
        data, sample_rate = sf.read('./output.wav')
        recognize_commands = RecognizeCommands(
            labels=["_silence_", "unknown", "yes", "no", "up", "down", "left", "right", "on", "off", "stop", "go"], #training label sequence
            average_window_duration_ms=1500,
            detection_threshold=0.7,
            suppression_ms=10,
            minimum_count=1)

        recognize_element = RecognizeResult()
        all_found_words = []
        data_samples = data.shape[0]
        recording_length = 1000 #in miliseconds
        clip_duration_samples = int(recording_length * sample_rate / 1000)
        clip_stride_samples = int(30 * sample_rate / 1000)
        audio_data_end = data_samples - clip_duration_samples

        # recognize_graph = self.load_graph("./model/my_frozen_graph.pb")
        recognize_graph = self.load_graph(self.model_list[0])

        with recognize_graph.as_default():
            with tf.compat.v1.Session() as sess:

                data_tensor = sess.graph.get_tensor_by_name("decoded_sample_data:0")
                sample_rate_tensor = sess.graph.get_tensor_by_name("decoded_sample_data:1")
                output_softmax_tensor = sess.graph.get_tensor_by_name("labels_softmax:0")

                for audio_data_offset in range(0, audio_data_end, clip_stride_samples):
                    input_start = audio_data_offset
                    input_end = audio_data_offset + clip_duration_samples
                    outputs = sess.run(
                        output_softmax_tensor,
                        feed_dict={
                            data_tensor:
                                np.expand_dims(data[input_start:input_end], axis=-1),
                            sample_rate_tensor:
                                sample_rate
                        })
                    outputs = np.squeeze(outputs)
                    current_time_ms = int(audio_data_offset * 1000 / sample_rate)
                    try:
                        recognize_commands.process_latest_result(outputs, current_time_ms,recognize_element)
                    except ValueError as e:
                        tf.compat.v1.logging.error('Recognition processing failed: {}' % e)
                        return
                    if (recognize_element.founded_command != '_silence_'):
                        all_found_words.append(recognize_element.founded_command)
                        return all_found_words
        return []