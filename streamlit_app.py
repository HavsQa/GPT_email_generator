import os
import openai
import streamlit as st

# DESIGN implement changes to the standard streamlit UI/UX
st.set_page_config(page_title="Octomail", page_icon="img/rephraise_logo.png",)
# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -4rem;}</style>''',
    unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-znku1x a {color: #F37748;}</style>''',
    unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-znku1x a {color: #F37748;}</style>''',
    unsafe_allow_html=True)  # lightmode
# Design change height of text input fields headers
st.markdown('''<style>.css-qrbaxs {min-height: 0.0rem;}</style>''',
    unsafe_allow_html=True)
# Design change spinner color to primary color
st.markdown('''<style>.stSpinner > div > div {border-top-color: #F37748;}</style>''',
    unsafe_allow_html=True)
# Design change min height of text input box
st.markdown('''<style>.css-15tx938{min-height: 0.0rem;}</style>''',
    unsafe_allow_html=True)
# Design hide top header line
hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
# Design hide "made with streamlit" footer menu area
hide_streamlit_footer = """<style>#MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_footer, unsafe_allow_html=True)


# Connect to OpenAI GPT-3, fetch API key from Streamlit secrets
openai.api_key = os.getenv("OPENAI_API_KEY")


def gen_mail_contents(email_contents):

    # iterate through all seperate topics
    for topic in range(len(email_contents)):
        input_text = email_contents[topic]
        rephrased_content = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Réécrivez le texte pour qu'il soit élaboré et poli.\nLes abréviations doivent être remplacées.\nTexte: {input_text}\nTexte réécrit:",
            # prompt=f"Rewrite the text to sound professional, elaborate and polite.\nText: {input_text}\nRewritten text:",
            temperature=0.8,
            max_tokens=len(input_text)*3,
            top_p=0.8,
            best_of=2,
            frequency_penalty=0.0,
            presence_penalty=0.0)

        # replace existing topic text with updated
        email_contents[topic] = rephrased_content.get("choices")[0]['text']
    return email_contents


def gen_mail_format(sender, recipient, style, email_contents):
    # update the contents data with more formal statements
    email_contents = gen_mail_contents(email_contents)
    # st.write(email_contents)  # view augmented contents

    contents_str, contents_length = "", 0
    for topic in range(len(email_contents)):  # aggregate all contents into one
        contents_str = contents_str + f"\nSujet{topic+1}: " + email_contents[topic]
        contents_length += len(email_contents[topic])  # calc total chars

    email_final_text = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Écrire un e-mail professionnel qui sonne {style} et inclut Sujet1 et Sujet2 dans cet ordre.\n\nExpéditeur: {sender}\nDestinataire: {recipient} {contents_str}\n\nEmail Text:",
        # prompt=f"Write a professional sounding email text that includes all of the following contents separately.\nThe text needs to be written to adhere to the specified writing styles and abbreviations need to be replaced.\n\nSender: {sender}\nRecipient: {recipient} {contents_str}\nWriting Styles: motivated, formal\n\nEmail Text:",
        temperature=0.8,
        max_tokens=contents_length*2,
        top_p=0.8,
        best_of=2,
        frequency_penalty=0.0,
        presence_penalty=0.0)

    return email_final_text.get("choices")[0]['text']


def main_gpt3emailgen():

    st.image('img/image_banner.png')  # TITLE and Creator information
    st.header('Optimisez votre efficacité et économisez précieusement votre temps en générant vos mails ! :alarm_clock: ')
    
    st.markdown("Je souhaite souligner que les coûts associés à l'utilisation de l'application, notamment ceux relatifs à l'API (gpt-3.5-turbo d'OpenAI), sont pris en charge de manière proactive. Cependant, si vous trouvez notre application bénéfique pour vos besoins et que vous souhaitez contribuer à son développement continu, nous accueillons toujours avec gratitude toute participation volontaire pour soutenir nos efforts. Merci !")
    st.write('\n')
    st.markdown("Guillaume M | [HavsQa](https://www.linkedin.com/in/guillaume-matilla-854228204/) | Prototype en vue d'une intégration dans un SaaS")
    st.markdown("Il est possible de générer du contenu (mails, articles..) avec votre plume, notamment pour de l'emailing automatisé. Contactez-moi pour plus d'infos!")
    st.write('\n')  # add spacing

    st.subheader('\nDe quoi parle votre e-mail ?\n')
    st.write(':red_circle: La qualité de la production étant intimement liée, il vaut mieux fournir un contexte minimal. Par exemple, il serait plus judicieux de dire "Transmettre le devis à Monsieur X" plutôt que simplement "envoi devis".')
    with st.expander("Corps du mail :inbox_tray:", expanded=True):

        input_c1 = st.text_input("Entrez le contenu de l'e-mail ci-dessous ! (actuellement 2 sujets séparés pris en charge)", 'Sujet 1')
        input_c2 = st.text_input('', 'Sujet 2 (optionnel)')

        email_text = ""  # initialize columns variables
        col1, col2, col3, space, col4 = st.columns([5, 5, 5, 0.5, 5])
        with col1:
            input_sender = st.text_input('Expéditeur', '')
        with col2:
            input_recipient = st.text_input('Destinataire', '')
        with col3:
            input_style = st.selectbox('Style',
                                       ('Formel', 'Motivé', 'Préoccupé', 'Déçu'),
                                       index=0)
        with col4:
            st.write("\n")  # add spacing
            st.write("\n")  # add spacing
            if st.button("C'est parti ! :incoming_envelope:"):
                with st.spinner(text="C'est dans le four..:fire:"):

                    input_contents = []  # let the user input all the data
                    if (input_c1 != "") and (input_c1 != 'topic 1'):
                        input_contents.append(str(input_c1))
                    if (input_c2 != "") and (input_c2 != 'topic 2 (optional)'):
                        input_contents.append(str(input_c2))

                    if (len(input_contents) == 0):  # remind user to provide data
                        st.write('Veuillez remplir certains contenus pour votre message !')
                    if (len(input_sender) == 0) or (len(input_recipient) == 0):
                        st.write("Les noms de l'expéditeur et du destinataire ne peuvent pas être vides !")

                    if (len(input_contents) >= 1):  # initiate gpt3 mail gen process
                        if (len(input_sender) != 0) and (len(input_recipient) != 0):
                            email_text = gen_mail_format(input_sender,
                                                         input_recipient,
                                                         input_style,
                                                         input_contents)
    if email_text != "":
        st.write('\n')  # add spacing
        st.subheader('\nVoici votre mail!\n')
        with st.expander("Votre mail :outbox_tray:", expanded=True):
            st.markdown(email_text)  #output the results


if __name__ == '__main__':
    # call main function
    main_gpt3emailgen()
