<template>
  <div v-if="quotes && quotes.length">
    <div class="question-container">
      <h2 class="question-text">{{ userQuestion }}</h2>
      <mdicon
        name="pencil"
        :size="27"
        class="edit-icon"
        @click="$emit('editQuery')"
      />
    </div>

    <div class="quotes-grid">
      <div v-for="(quote, index) in parsedQuotes" 
           :key="index" 
           class="quote-card">
        <p class="quote-text">{{ quote.quoteText }}</p>
        <p class="author-text">{{ quote.philosopher }}</p>
        <p class="book-text">{{ quote.source }} {{ quote.year ? `(${quote.year})` : '' }}</p>
        <button class="learn-more-btn" @click="handleLearnMore(quote)">Learn More</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ShowQuote',
  props: {
    quotes: {
      type: Array,
      required: true
    },
    userQuestion: {
      type: String,
      required: true
    }
  },
  mounted() {
    console.log('ShowQuote mounted:', {
      quotes: this.quotes,
      userQuestion: this.userQuestion
    });
  },
  methods: {
    handleLearnMore(quote) {
      console.log('handleLearnMore called:', {
        quote,
        currentRoute: this.$route.name
      });
      // Ensure all required data is available
      if (!quote.quoteText || !quote.philosopher || !quote.source || !this.userQuestion) {
        console.error('Missing required data for navigation');
        return;
      }

      const query = {
        quote: quote.quoteText,
        philosopher: quote.philosopher,
        source: quote.source,
        year: quote.year || '-',
        userQuestion: this.userQuestion
      };
      
      try {
        this.$router.push({
          name: 'LearnMore',
          query
        })
      } catch (error) {
        console.error('Router error:', error);
      }
    }
  },
  computed: {
    parsedQuotes() {
      return this.quotes.map(quote => {
        // Split on '" -' to separate quote from attribution
        const [quotePart, attribution] = quote.split('" -').map(s => s.trim())
        // Get the quote text without surrounding quotes
        const quoteText = quotePart.replace(/^"|"$/g, '')
        
        // Parse attribution part: "PHILOSOPHER, SOURCE, YEAR -"
        const [philosopher, ...rest] = attribution.split(',').map(s => s.trim())
        // Remove trailing dash and split remaining into source and year
        const [source, year] = rest.join(',').replace(/-$/, '').split(',').map(s => s.trim())
        
        return {
          quoteText,
          philosopher,
          source: source?.replace(/^"|"$/g, ''), // Remove quotes from source
          year: year || ''
        }
      })
    }
  }
}
</script>

<style scoped>
.question-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 30px;
  width: 100%;
}

.question-text {
  color: #000000;
  font-size: 18px;
  font-weight: 500;
  line-height: 22px;
  text-align: center;
  margin: 0;
}

.edit-icon {
  color: #a9d5fe;
  font-size: 15px;
  width: 20px;
  height: 17px;
  cursor: pointer;
  margin-left: 2px;
  margin-bottom: 12px;
}

.quotes-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.quote-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  min-height: 250px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.quote-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.quote-text {
  color: #1f2937;
  font-size: 15px;
  font-style: italic;
  line-height: 1.5;
  text-align: center;
  margin-bottom: 10px;
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.author-text {
  color: #1f2937;
  font-size: 14px;
  line-height: 1.4;
  text-align: center;
  margin-bottom: 10px;
}

.book-text {
  color: #666;
  font-size: 12px;
  text-align: center;
  margin-bottom: 15px;
}

.learn-more-btn {
  display: block;
  width: 100%;
  padding: 8px;
  background-color: #030303;
  border: none;
  border-radius: 4px;
  color: #ffffff;
  font-size: 14px;
  line-height: 1.4;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.3s;
}

.learn-more-btn:hover {
  background-color: #e5e7eb;
}

@media (max-width: 768px) {
  .quotes-grid {
    grid-template-columns: 1fr;
    max-width: 500px;
  }

  .quote-card {
    min-height: 200px;
  }
}
</style>