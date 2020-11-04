from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tensorflow.python.ops import io_ops
import numpy as np

from model.recognize_commands import RecognizeResult, RecognizeCommands


class Recognizer:

    def __init__(self):
        super().__init__()
        # Import trained model
        # self.model = tf.import_graph_def(self.load_graph("./model/my_frozen_graph.pb"), return_elements=[
        #                                         'data/inputs:0',
        #                                         'output/network_activation:0',
        #                                         'data/correct_outputs:0'],
        #                                         name='')
        # print("In init: ", self.model)

    def classifyCommand(self, command):
        commandClass = "silence"
        # identify command
        # print("Model: ", self.model)
        # self.model(command)
        # print("Recognized command: ", command)

        # print("Recognized: ", self.recognize())
        commands = self.recognize()
        if len(commands) > 0:
            commandClass = commands[0]
        return commandClass

    def load_graph(self, frozen_graph_filename):
        # with tf.io.gfile.GFile(frozen_graph_filename, "rb") as f:
        #     graph_def = tf.compat.v1.GraphDef()
        #     graph_def.ParseFromString(f.read())
        #     print("Returning graph: ")
        #     return graph_def

        """Read a tensorflow model, and creates a default graph object."""
        graph = tf.Graph()
        with graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(frozen_graph_filename, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        return graph

    def read_wav_file(self, filename):
        """Load a wav file and return sample_rate and numpy data of float64 type."""
        with tf.compat.v1.Session(graph=tf.Graph()) as sess:
            wav_filename_placeholder = tf.compat.v1.placeholder(tf.string, [])
            wav_loader = io_ops.read_file(wav_filename_placeholder)
            wav_decoder = tf.audio.decode_wav(wav_loader, desired_channels=1)
            res = sess.run(wav_decoder, feed_dict={wav_filename_placeholder: filename})
            # print("SR: ", res.sample_rate)
        return res.sample_rate, res.audio.flatten()

    def recognize(self):
        sample_rate, data = self.read_wav_file("./output.wav")
        recognize_commands = RecognizeCommands(
            labels=["_silence_", "unknown", "yes", "no", "up", "down", "left", "right", "on", "off", "stop", "go"], #training label sequence
            average_window_duration_ms=2000,
            detection_threshold=0.7,
            suppression_ms=10,
            minimum_count=1)

        recognize_element = RecognizeResult()
        all_found_words = []
        data_samples = data.shape[0]
        recording_length = 1000 #in miliseconds
        clip_duration_samples = int(recording_length * sample_rate / 1000)
        clip_stride_samples = int(recording_length * sample_rate / 1000)
        audio_data_end = data_samples - clip_duration_samples

        # print("audio_data_end:", audio_data_end, "clip_stride_samples:", clip_stride_samples)

        # Load model and create a tf session to process audio pieces
        recognize_graph = self.load_graph("./model/my_frozen_graph.pb")
        with recognize_graph.as_default():
            with tf.compat.v1.Session() as sess:

                # Get input and output tensor
                data_tensor = sess.graph.get_tensor_by_name("decoded_sample_data:0")
                sample_rate_tensor = sess.graph.get_tensor_by_name("decoded_sample_data:1")
                output_softmax_tensor = sess.graph.get_tensor_by_name("labels_softmax:0")

                # Inference along audio stream.
                for audio_data_offset in range(0, audio_data_end, clip_stride_samples):
                    # print("Recognizing")
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
                        recognize_commands.process_latest_result(outputs, current_time_ms,
                                                                 recognize_element)
                    except ValueError as e:
                        tf.compat.v1.logging.error('Recognition processing failed: {}' % e)
                        return
                    # print("Recognize element: ", recognize_element.founded_command)
                    if (recognize_element.founded_command != '_silence_'):
                        all_found_words.append(recognize_element.founded_command)
        return all_found_words