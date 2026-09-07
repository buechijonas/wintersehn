export const legalPages = {
  impressum: {
    title: 'Impressum',
    illustration: 'impressum',
    intro: 'Verantwortlich für den Inhalt gemäss §5 TMG (Telemetriegesetz) und Art. 4 Abs. 7 DSGVO',
    sections: [
      { address: true },
      {
        title: 'Haftung für Inhalte',
        text: `Die Inhalte unserer Seite wurden mit grösster Sorgfalt erstellt. Für die Richtigkeit,
          Vollständigkeit und Aktualität der Inhalte können wir jedoch keine Gewähr übernehmen.`,
      },
      {
        title: 'Obligatorischer Hinweis',
        text: `Diese Webapplikation gehört Wintersehn. Der Hinweis ist hier aufgrund der geltenden
          Impressumspflicht der Europäischen Union und der Schweiz enthalten.`,
      },
    ],
  },

  privacy: {
    title: 'Datenschutzerklärung',
    breadcrumbLabel: 'Datenschutzerklärung',
    illustration: 'privacy',
    sections: [
      { title: '1. Verantwortliche Stelle', address: true },
      {
        title: '2. Zweck der Datenverarbeitung',
        text: `Dieses Projekt ist ein rein freizeitliches Vorhaben, das ausschliesslich der Weiterbildung
          und Wissensvermittlung dient. Die Nutzung der Webapplikation setzt voraus, dass die
          Verarbeitung personenbezogener Daten im Rahmen der Verwaltung durch mich akzeptiert wird.
          Nutzer, die dieser Regelung nicht zustimmen möchten, sind eingeladen, die Plattform nicht
          weiter zu verwenden.`,
      },
      {
        title: '3. Erhobene Daten',
        text: `Beim Besuch unserer Webapplikation werden automatisch Informationen durch den Webserver in
          sogenannten Log-Dateien gespeichert. Diese beinhalten die IP-Adresse, den Browsertyp, das
          Betriebssystem, die Referrer-URL, potenziell Teile des Browserverlaufs sowie das Datum und die
          Uhrzeit des Zugriffs. Diese Daten werden nicht weitergegeben.`,
      },
      {
        title: '4. Rechtsgrundlage',
        text: `Die Verarbeitung der genannten Daten erfolgt gemäss Art. 6 Abs. 1 lit. f DSGVO, wobei unser
          berechtigtes Interesse darin besteht, eine funktionsfähige und benutzerfreundliche
          Webapplikation zu betreiben.`,
      },
      {
        title: '5. Dauer der Speicherung',
        text: `Personenbezogene Daten werden nur so lange gespeichert, wie dies für die Erreichung der hier
          genannten Zwecke erforderlich ist, jedoch nach einer Deaktivierung des Kontos maximal für eine
          Dauer von 10 Jahren.`,
      },
      {
        title: '6. Weitergabe an Dritte',
        text: 'Es wird versucht, keine personenbezogenen Daten an Dritte weiterzugeben.',
      },
      {
        title: '7. Rechte der betroffenen Personen',
        text: `Sie haben das Recht, Auskunft über die von uns verarbeiteten personenbezogenen Daten zu
          erhalten, sowie Berichtigung, Löschung oder Einschränkung der Verarbeitung zu verlangen. Zudem
          können Sie der Verarbeitung Ihrer personenbezogenen Daten widersprechen. Bitte wenden Sie sich
          dazu an die oben angegebene Kontaktadresse.`,
      },
      {
        title: '8. Änderung der Datenschutzerklärung',
        text: `Wir behalten uns vor, diese Datenschutzerklärung zu ändern, um sie an aktuelle rechtliche
          Anforderungen oder Änderungen unserer Leistungen anzupassen. Die jeweils aktuelle Fassung ist
          jederzeit auf dieser Webapplikation abrufbar.`,
      },
    ],
  },

  terms: {
    title: 'Nutzungsrichtlinien',
    breadcrumbLabel: 'Nutzungsrichtlinien',
    illustration: 'terms',
    sections: [
      {
        title: '1. Allgemeine Grundsätze',
        text: `Diese Webapplikation ist ein freizeitliches Vorhaben, das ausschliesslich der Weiterbildung
          und Wissensvermittlung dient. Die Nutzung der Webapplikation unterliegt diesen Nutzungsrichtlinien,
          die jederzeit von der Verantwortlichen angepasst werden können. Mit der Nutzung der Webapplikation
          stimmen Sie diesen Nutzungsrichtlinien zu.`,
      },
      {
        title: '2. Strafrechtliche Verfolgung',
        text: `Die Nutzung dieser Webapplikation setzt die Einhaltung der geltenden europäischen und
          schweizerischen Gesetze voraus. Verstösse wie z. B. Cybermobbing, Datendiebstahl oder andere
          rechtswidrige Handlungen werden mit voller Härte strafrechtlich verfolgt. In solchen Fällen werden
          sämtliche personenbezogenen und hochsensiblen Daten an die zuständigen Behörden weitergeleitet, um
          die Verfolgung und Ahndung solcher Straftaten sicherzustellen.`,
      },
      {
        title: '3. Verhaltensregeln',
        text: `Um eine sichere und respektvolle Umgebung für alle Benutzer zu gewährleisten, sind die
          folgenden Verhaltensweisen auf dieser Webapplikation strengstens untersagt:`,
        items: [
          {
            title: 'Antisemitismus',
            description: 'Jegliche Form von antisemitischer Äusserung oder Handlung.',
          },
          {
            title: 'Ausbeuterische Inhalte',
            description: 'Inhalte, die auf die Ausbeutung von Menschen oder Tieren abzielen.',
          },
          {
            title: 'Ausweichung von Minderjährigenschutz',
            description: `Handlungen, die gegen den Schutz von Minderjährigen verstossen, wie z. B.
              unzulässiger Kontakt.`,
          },
          {
            title: 'Beleidigung',
            description: 'Gebrauch von abwertender, beleidigender oder vulgärer Sprache.',
          },
          {
            title: 'Belohnungsjagd',
            description: 'Unrechtmässiges Ausnutzen von Funktionen der Plattform.',
          },
          {
            title: 'Belästigung',
            description: 'Unangemessene Annäherung, Kontaktaufnahme oder Nachstellung.',
          },
          {
            title: 'Betrug',
            description: 'Täuschung oder betrügerisches Verhalten zum Zweck der Bereicherung.',
          },
          {
            title: 'Christophobie',
            description: 'Feindseligkeit oder Vorurteile gegenüber Christen oder dem Christentum.',
          },
          {
            title: 'Cybergrooming',
            description: `Versuche, Kinder online zu manipulieren oder zu missbrauchen. Erwachsene, die
              versuchen, sich Kindern auf dieser Plattform anzunähern, werden nicht toleriert.`,
          },
          {
            title: 'Diskriminierung',
            description: `Benachteiligung oder Herabwürdigung von Personen aufgrund von Geschlecht, Rasse,
              Religion, sexueller Orientierung oder anderen persönlichen Merkmalen.`,
          },
          {
            title: 'Doxxing',
            description: `Veröffentlichung oder Weitergabe von privaten Informationen ohne Zustimmung der
              betroffenen Person.`,
          },
          {
            title: 'Drohung',
            description: 'Androhung von Gewalt, Mord oder anderen negativen Konsequenzen.',
          },
          {
            title: 'Erpressung',
            description:
              'Jede Handlung, bei der eine Person durch Androhung von Nachteilen zu etwas gezwungen wird.',
          },
          {
            title: 'Falschinformationen',
            description: 'Verbreitung von falschen oder irreführenden Informationen.',
          },
          {
            title: 'Faschismus',
            description: 'Förderung oder Verbreitung faschistischer Ideologien.',
          },
          {
            title: 'Fremdenfeindlichkeit',
            description:
              'Feindseligkeit oder Vorurteile gegenüber Ausländern oder ethnischen Minderheiten.',
          },
          {
            title: 'Gefährliche Verschwörungstheorien',
            description:
              'Verbreitung oder Unterstützung von Theorien, die Panik, Angst oder Gewalt fördern können.',
          },
          {
            title: 'Gewaltbasierter Inhalt',
            description: 'Verbreitung von Inhalten, die Gewalt fördern oder darstellen.',
          },
          {
            title: 'Gewaltverherrlichung',
            description:
              'Förderung oder Rechtfertigung von Gewalt gegen Einzelpersonen, Gruppen oder Institutionen.',
          },
          {
            title: 'Hassrede',
            description: 'Äusserungen, die zu Hass oder Gewalt gegen bestimmte Gruppen aufrufen.',
          },
          {
            title: 'Homophobie',
            description: 'Feindseligkeit oder Vorurteile gegenüber homosexuellen Personen.',
          },
          {
            title: 'Identitätsdiebstahl',
            description:
              'Falsche Darstellung oder Ausgeben als eine andere Person, Institution oder Entität.',
          },
          {
            title: 'Illegale Inhalte',
            description:
              'Verbreitung oder Bereitstellung von Inhalten, die gegen geltendes Recht verstossen.',
          },
          {
            title: 'Islamophobie',
            description: 'Feindseligkeit oder Vorurteile gegenüber Muslimen oder dem Islam.',
          },
          {
            title: 'Kulturelle Aneignung',
            description:
              'Unangemessene Nutzung oder Darstellung von kulturellen Symbolen, Traditionen oder Werten.',
          },
          {
            title: 'Missbrauch von Privilegien',
            description: `Jegliche Form von ungerechtfertigter Ausnutzung von Rechten oder Zugriffsrechten
              auf dieser Webapplikation.`,
          },
          {
            title: 'Plagiate',
            description: `Hochladen oder Teilen von Inhalten, die ohne Zustimmung von Dritten kopiert oder
              vervielfältigt wurden.`,
          },
          {
            title: 'Pornografische Inhalte',
            description: `Verbreitung, Bereitstellung oder Zugänglichmachung von pornografischen oder
              sexuellen Inhalten.`,
          },
          {
            title: 'Propaganda',
            description: `Verbreitung von politisch oder ideologisch einseitigen Informationen zu
              Manipulationszwecken.`,
          },
          {
            title: 'Rassismus',
            description:
              'Diskriminierung oder Feindseligkeit gegenüber Personen aufgrund ihrer ethnischen Herkunft.',
          },
          {
            title: 'Selbstgefährdung',
            description: `Inhalte oder Verhaltensweisen, die zu Selbstverletzung oder suizidalem Verhalten
              ermutigen oder dieses fördern. Wir bitten darum, stattdessen dazu zu ermutigen, sich Hilfe zu
              suchen und mit jemandem darüber zu sprechen.`,
          },
          {
            title: 'Selbstjustiz',
            description: `Förderung oder Verherrlichung von Handlungen, die darauf abzielen, Recht in die
              eigene Hand zu nehmen.`,
          },
          {
            title: 'Sexismus',
            description: `Diskriminierung oder Herabwürdigung aufgrund des Geschlechts. Das gilt in beide
              Richtungen, sowohl Misogynie als auch Misandrie.`,
          },
          {
            title: 'Sextortion',
            description:
              'Erpressung unter Androhung, private oder intime Informationen zu veröffentlichen.',
          },
          {
            title: 'Spam',
            description:
              'Unerwünschte und unaufgeforderte Nachrichten, insbesondere Werbenachrichten.',
          },
          {
            title: 'Unangemessene Wortwahl',
            description:
              'Verwendung von respektlosen, beleidigenden oder unangemessenen Ausdrücken.',
          },
          {
            title: 'Unethische Werbung',
            description: `Bewerbung von Produkten, Dienstleistungen oder Inhalten, die betrügerisch,
              unethisch oder schädlich sind.`,
          },
        ],
      },
      {
        title: '4. Änderung der Nutzungsrichtlinien',
        text: `Die Nutzungsrichtlinien können jederzeit ohne vorherige Ankündigung geändert werden. Nutzer
          werden gebeten, die Richtlinien regelmässig zu überprüfen, um auf dem neusten Stand zu bleiben.`,
      },
      {
        title: '5. Geistiges Eigentum',
        text: `Alle Inhalte auf dieser Plattform, einschliesslich Texte, Bilder, Grafiken, Logos und
          Software, sind urheberrechtlich geschützt. Die Vervielfältigung, Verbreitung oder Verwendung der
          Inhalte ohne ausdrückliche Genehmigung ist untersagt.`,
      },
      {
        title: '6. Missbrauchsmeldung',
        text: `Wenn Sie Verstösse gegen die Nutzungsrichtlinien oder missbräuchliches Verhalten
          feststellen, sind Sie verpflichtet, dies unverzüglich über die vorgesehenen Meldewege zu melden.
          Sollte dies nicht geschehen, verstossen Sie gegen die Nutzungsrichtlinien.`,
      },
    ],
  },

  disclaimer: {
    title: 'Haftungsausschluss',
    breadcrumbLabel: 'Haftungsausschluss',
    illustration: 'disclaimer',
    sections: [
      {
        title: '1. Inhalt des Onlineangebots',
        text: `Die Inhalte dieser Webapplikation wurden mit grösstmöglicher Sorgfalt entwickelt. Für die
          Richtigkeit, Vollständigkeit und Aktualität der Inhalte können wir jedoch keine Gewähr übernehmen.
          Als Dienstanbieter sind wir gemäss § 7 Abs. 1 TMG für eigene Inhalte auf diesen Seiten nach den
          allgemeinen Gesetzen verantwortlich. Nach § 8 bis 10 TMG sind wir jedoch nicht verpflichtet,
          übermittelte oder gespeicherte fremde Informationen zu überwachen oder nach Umständen zu forschen,
          die auf eine rechtswidrige Tätigkeit hinweisen, wenn sie sich auf einer externen Plattform befinden.
          Verpflichtungen zur Entfernung oder Sperrung der Nutzung von uns erstellten Informationen nach den
          allgemeinen Gesetzen bleiben hiervon unberührt. Eine diesbezügliche Haftung ist jedoch erst ab dem
          Zeitpunkt der Kenntnis einer konkreten Rechtsverletzung möglich. Bei Bekanntwerden von
          entsprechenden Rechtsverletzungen werden wir diese Inhalte umgehend entfernen.`,
      },
      {
        title: '2. Haftung für Links',
        text: `Unser Angebot enthält Links zu externen Webseiten Dritter, auf deren Inhalte wir keinen
          Einfluss haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen. Für die
          Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der Seiten
          verantwortlich. Eine permanente inhaltliche Kontrolle der verlinkten Seiten ist jedoch ohne
          konkrete Anhaltspunkte einer Rechtsverletzung nicht zumutbar. Bei Bekanntwerden von
          Rechtsverletzungen werden wir derartige Links umgehend entfernen.`,
      },
      {
        title: '3. Urheberrecht',
        text: `Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem
          deutschen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art von Verwertung
          ausserhalb der Grenzen des Urheberrechts bedürfen der schriftlichen Zustimmung des jeweiligen
          Autors bzw. Erstellers. Downloads und Kopien dieser Seiten sind nur für den privaten Gebrauch
          gestattet. Soweit die Inhalte auf dieser Seite nicht vom Betreiber erstellt wurden, werden die
          Urheberrechte Dritter beachtet, insbesondere werden Inhalte Dritter als solche gekennzeichnet.
          Sollten Sie trotzdem auf eine Urheberrechtsverletzung aufmerksam werden, bitten wir um einen
          entsprechenden Hinweis. Bei Bekanntwerden von Rechtsverletzungen werden wir derartige Inhalte
          umgehend entfernen.`,
      },
      {
        title: '4. Haftung für Schäden',
        text: `Wir schliessen jegliche Haftung für Schäden aus, die direkt oder indirekt aus der Nutzung
          dieser Webapplikation und der darin enthaltenen Informationen entstehen, soweit diese nicht auf
          Vorsatz oder grober Fahrlässigkeit beruhen.`,
      },
      {
        title: '5. Keine Abmahnung ohne vorherigen Kontakt',
        text: `Sollten Inhalte dieser Webapplikation die Rechte Dritter oder gesetzliche Bestimmungen
          verletzen, bitten wir um eine entsprechende Nachricht ohne Kostennote. Wir garantieren, dass die zu
          Recht beanstandeten Inhalte analysiert und evaluiert werden, ohne dass die Einschaltung eines
          Rechtsbeistandes erforderlich ist. Dennoch von Ihnen ohne vorherige Kontaktaufnahme ausgelöste
          Kosten werden wir vollständig zurückweisen und gegebenenfalls Gegenklage wegen Verletzung
          vorgenannter Bestimmungen erheben.`,
      },
    ],
  },
}
