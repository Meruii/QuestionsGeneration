import json
import os
from corpus import Corpus
import io


def add_annotations_from_frame(annot, f, txt_index):
    for _, frame_element in f.frame_elements.items():
        if frame_element.mention:
            continue
        new_annot = {'id': txt_index, 'lu_index': f.index, 'frame': f.semantic_frame,
                     'lu': None,'frame_elements': []}
        for _,other_fe in f.frame_elements.items():
            if other_fe.name == frame_element.name:
                continue
            if other_fe.mention:
                new_annot['lu'] = other_fe.name
                continue
            fe_data = {'name': other_fe.name, 'text': other_fe.get_string_of_superficial_form(),
                       'coref': other_fe.get_string_of_coref()}
            new_annot['frame_elements'].append(fe_data)
        new_annot['answer'] = {'name': frame_element.name, 'text': frame_element.get_string_of_superficial_form(),
                               'coref': frame_element.get_string_of_coref()}
        new_annot['questions'] = []
        annot.append(new_annot)
    return annot


if __name__ == "__main__":

    # corpus_dir_name = "../data/Corpus/corefsCorpus"
    # json_dir_name = "../data/Corpus/json"
    # for fname in os.listdir(corpus_dir_name):
    #     corpus = Corpus(os.path.join(corpus_dir_name, fname), fname)
    #     json_file_name = os.path.join(json_dir_name, fname) + '/' + corpus.name + ".json"
    #     outfile = io.open(json_file_name, "w", encoding='utf8')
    #     annotations = []
    #     for _, t in corpus.texts.items():
    #         for _, frame in t.frames.items():
    #             annotations = add_annotations_from_frame(annotations, frame, t.name)
    #     data = {'annotations': annotations}
    #     json_data = json.dump(data, outfile, indent=4, ensure_ascii=False)

    corpus_dir_name = "../data/Corpus/corefsCorpus"

    outfile = io.open("../data/Corpus/json/annotations.json", "w", encoding='utf8')
    annotations = []
    corpus = []

    for fname in os.listdir(corpus_dir_name):
        corpus.append(Corpus(os.path.join(corpus_dir_name, fname), fname))

    for c in corpus:
        for _, t in c.texts.items():
            for _, frame in t.frames.items():
                annotations = add_annotations_from_frame(annotations, frame, t.name)
    data = {'annotations': annotations}
    json_data = json.dump(data, outfile, indent=4, ensure_ascii=False)
