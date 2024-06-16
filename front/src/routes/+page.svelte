


 <script>
  import { onMount } from 'svelte';

  class Party {
      constructor(name, ayes, nays, color) {
          this.name = name;
          this.ayes = ayes;
          this.nays = nays;
          this.color = color;
      }
  }

  class Vote {
      constructor(title, parties, summary, questions) {
          this.title = title;
          this.parties = parties;
          this.summary = summary;
          this.questions = questions;

          this.processParties();
      }

      processParties() {
          this.totalAyes = this.parties.reduce((sum, party) => sum + party.ayes, 0);
          this.totalNays = this.parties.reduce((sum, party) => sum + party.nays, 0);
      }

      getBarWidth(votes, total) {
          return total ? (votes / total) * 100 : 0;
      }

      getBarTextRepresentation() {
          return this.parties.map(party => `${party.name} had ${party.ayes} ayes and ${party.nays} nays`).join(', ');
      }
  }

  let query = "";
  let voteArr = [];
  let index = 0;

  function next() {
      if (index < voteArr.length - 1) {
          index += 1;
          displayVote(voteArr[index]);
      }
  }

  function prev() {
      if (index > 0) {
          index -= 1;
          displayVote(voteArr[index]);
      }
  }

  function displayVote(vote) {
      const cardContainer = document.getElementById('cardContainer');
      cardContainer.innerHTML = ''; // Reset card container

      const card = document.createElement('div');
      card.className = 'bg-white shadow-md rounded-lg p-6 mb-6';

      const title = document.createElement('h3');
      title.className = 'text-xl font-bold mb-2';
      title.textContent = vote.title;
      card.appendChild(title);

      const summary = document.createElement('p');
      summary.className = 'text-gray-700 mb-4';
      summary.textContent = vote.summary;
      card.appendChild(summary);

      ['Ayes', 'Nays'].forEach(type => {
          const barContainer = document.createElement('div');
          barContainer.className = 'flex items-center mb-4';

          const label = document.createElement('div');
          label.className = 'mr-4 font-bold';
          label.textContent = type;
          barContainer.appendChild(label);

          vote.parties.forEach(party => {
              const bar = document.createElement('div');
              bar.className = 'bar-section h-6 mx-1';
              bar.style.width = `${type === 'Ayes' ? vote.getBarWidth(party.ayes, vote.totalAyes) : vote.getBarWidth(party.nays, vote.totalNays)}%`;
              bar.style.backgroundColor = party.color;
              barContainer.appendChild(bar);
          });

          card.appendChild(barContainer);
      });

      const barText = document.createElement('p');
      barText.className = 'text-sm text-gray-500 mb-4';
      barText.textContent = vote.getBarTextRepresentation();
      card.appendChild(barText);

      const questions = document.createElement('div');
      questions.className = 'questions mb-4';
      vote.questions.forEach(q => {
          const question = document.createElement('p');
          question.className = 'font-semibold text-left';
          question.textContent = `Question: ${q.question}`;
          questions.appendChild(question);

          const answer = document.createElement('p');
          answer.className = 'text-sm text-gray-600 text-left';
          answer.textContent = `Answer: ${q.answer}`;
          questions.appendChild(answer);
      });
      card.appendChild(questions);

      cardContainer.appendChild(card);
  }

  function getRelatedVotes(query) {
      var dummyData = [
          {
              niceTitle: "Simplified Immigration Appeal Process for Suspensive Claims",
              summary: "This legislation amends the rules for how immigration and asylum appeals are handled in the UK, specifically for suspensive claims. Suspensive claims are appeals made by individuals against removal from the UK, arguing that their removal should be paused. The new rules streamline the process, ensuring faster decisions and clarifying the steps for both applicants and the authorities.",
              questions: [
                  { question: "What is a suspensive claim?", answer: "A suspensive claim is an appeal made by an individual to pause their removal from the UK, arguing that their removal would be unjust or unsafe." },
                  { question: "What changes if this bill passes?", answer: "The appeal process for suspensive claims will become quicker and more structured. New timelines and specific procedures will be introduced to ensure prompt decisions by the Upper Tribunal." },
                  { question: "How will this affect individuals facing removal?", answer: "Individuals will have clear guidelines on how to submit their appeals and what information is required. The process will be more transparent, and decisions will be made within set timeframes, reducing uncertainty for those appealing their removal." }
              ],
              parties: [
                  { party: "Conservative", color: "blue", ayes: 133, noes: 0 },
                  { party: "Labour", color: "red", ayes: 0, noes: 0 }
              ]
          }
      ];
      dummyData = [
    {
      "title": "The Tribunal Procedure (Upper Tribunal) (Immigration and Asylum Chamber) (Amendment) Rules 2024",
      "niceTitle": "Simplified Immigration Appeal Process for Suspensive Claims",
      "summary": "This legislation amends the rules for how immigration and asylum appeals are handled in the UK, specifically for suspensive claims. Suspensive claims are appeals made by individuals against removal from the UK, arguing that their removal should be paused. The new rules streamline the process, ensuring faster decisions and clarifying the steps for both applicants and the authorities.",
      "questions": [
        {
          "question": "What is a suspensive claim?",
          "answer": "A suspensive claim is an appeal made by an individual to pause their removal from the UK, arguing that their removal would be unjust or unsafe."
        },
        {
          "question": "What changes if this bill passes?",
          "answer": "The appeal process for suspensive claims will become quicker and more structured. New timelines and specific procedures will be introduced to ensure prompt decisions by the Upper Tribunal."
        },
        {
          "question": "How will this affect individuals facing removal?\n\n",
          "answer": "Individuals will have clear guidelines on how to submit their appeals and what information is required. The process will be more transparent, and decisions will be made within set timeframes, reducing uncertainty for those appealing their removal."
        }
      ],
      "parties": [
        {
          "party": "Conservative",
          "color": "blue",
          "ayes": 133,
          "noes": 10
        },
        {
          "party": "Labour",
          "color": "red",
          "ayes": 60,
          "noes": 3
        }
      ]
    },
    {
      "title": "Finance (No. 2) Bill",
      "niceTitle": "Finance Act 2024: Tax Changes and Property Adjustments",
      "summary": "The Finance Act 2024 introduces new income tax rates, adjusts thresholds for child benefit charges, and modifies capital gains tax on property. It also abolishes multiple dwellings relief for Stamp Duty Land Tax (SDLT) and makes changes to the tax treatment of certain financial and property transactions.",
      "questions": [
        {
          "question": "What are the new income tax rates for the 2024-25 tax year?",
          "answer": "The basic rate is 20%.\nThe higher rate is 40%.\nThe additional rate is 45%.\n"
        },
        {
          "question": "How does the Act affect child benefit charges?",
          "answer": "The income thresholds for the high-income child benefit charge have increased to £60,000 and £80,000. This means families earning below these thresholds may now receive more child benefit without incurring additional tax charges."
        },
        {
          "question": "What changes are being made to property taxes?",
          "answer": "The higher capital gains tax rate for residential property gains is reduced to 24%.\nThe multiple dwellings relief for SDLT is abolished, impacting transactions involving multiple properties.\nFirst-time buyers' relief for SDLT now includes acquisitions of new leases on bare trust, making it easier for first-time buyers to qualify."
        }
      ],
      "parties": [
        {
          "party": "Conservative",
          "color": "blue",
          "ayes": 211,
          "noes": 4
        },
        {
          "party": "Labour",
          "color": "red",
          "ayes": 30,
          "noes": 1
        }
      ]
    },
    {
      "title": "High Speed Rail (Crewe - Manchester) Bill: Instruction (No. 3)",
      "niceTitle": "High Speed Rail Expansion: West Midlands to Crewe",
      "summary": "This legislation authorizes the construction and maintenance of a new high-speed rail line (Phase 2a of High Speed 2) connecting the West Midlands to Crewe. It provides the necessary legal framework for land acquisition, environmental measures, and construction processes required to extend the high-speed rail network.",
      "questions": [
        {
          "question": "What is the main purpose of this legislation?",
          "answer": "The legislation enables the construction of a high-speed rail line from the West Midlands to Crewe, enhancing the UK's transportation network and reducing travel times between major cities."
        },
        {
          "question": "How will the construction affect local residents?",
          "answer": "There will be significant construction activity, which may cause temporary disruptions. The legislation includes measures to mitigate environmental impacts and provide compensation to affected landowners."
        },
        {
          "question": "What are the benefits of this new rail line?",
          "answer": "The new rail line will provide faster travel between the West Midlands and Crewe, improve connectivity, and support economic growth by making it easier for people to commute and for goods to be transported efficiently."
        }
      ],
      "parties": [
        {
          "party": "Conservative",
          "color": "blue",
          "ayes": 222,
          "noes": 5
        },
        {
          "party": "Labour",
          "color": "red",
          "ayes": 86,
          "noes": 2
        }
      ]
    },
    {
      "title": "Digital Markets, Competition and Consumers Bill: Consideration of Lords Message: manuscript amendment",
      "niceTitle": "Digital Market Competition and Consumer Protection Act 2024",
      "summary": "This legislation aims to regulate competition within digital markets, ensuring fair practices and protecting consumers. It grants the Competition and Markets Authority (CMA) the power to oversee large digital companies, imposing requirements to prevent unfair competition and promote transparency.",
      "questions": [
        {
          "question": "What is the main goal of this Act?",
          "answer": "The primary goal is to regulate large digital companies to ensure they don't engage in unfair practices that harm competition or consumers. This includes monitoring their behavior, imposing rules for fair conduct, and taking action if they abuse their market power.\n"
        },
        {
          "question": "How will this Act affect big digital companies?\n\n",
          "answer": "Big digital companies may be designated as having strategic market status (SMS), which subjects them to specific conduct requirements. These requirements aim to ensure fair trading, transparency, and prevent them from using their dominant position to stifle competition."
        },
        {
          "question": "",
          "answer": ""
        }
      ],
      "parties": [
        {
          "party": "Conservative",
          "color": "blue",
          "ayes": 5,
          "noes": 259
        },
        {
          "party": "Labour",
          "color": "red",
          "ayes": 164,
          "noes": 10
        }
      ]
    }
  ];

      return dummyData.map(vote => new Vote(vote.niceTitle, vote.parties.map(p => new Party(p.party, p.ayes, p.noes, p.color)), vote.summary, vote.questions));
  }

  function handleSubmit() {
      voteArr = getRelatedVotes(query);
      index = 0; // Reset index to 0 when new search is made
      displayVote(voteArr[index]);
  }
</script>

<style>
  .bar-section {
      transition: width 0.3s ease;
  }
</style>

<main class="text-center p-4 bg-gray-100 min-h-screen">
  <header class="bg-blue-500 text-white p-4 rounded-lg flex items-center justify-center">
    <img src="/logo.png" alt="Logo" class="h-[150px] w-[150px] mr-4" />
    <h1 class="text-2xl">Ultimate Vote Searcher</h1>
  </header>

  <div class="my-4">
      <h2 class="text-lg">Enter what you care about!</h2>
      <input type="text" id="query" class="border p-2 rounded-lg" bind:value={query} placeholder="Sewage..." />
      <button class="bg-blue-500 text-white p-2 ml-2 rounded-lg" on:click={handleSubmit}>Submit</button>
  </div>

  <div id="cardContainer" class="my-4"></div>

  <div class="flex justify-center mt-4">
      <button class="bg-blue-500 text-white p-2 mx-2 rounded-lg" on:click={prev}>Previous</button>
      <button class="bg-blue-500 text-white p-2 mx-2 rounded-lg" on:click={next}>Next</button>
  </div>
</main>
