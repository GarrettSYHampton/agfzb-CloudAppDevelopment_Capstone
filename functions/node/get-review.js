const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");

async function main(params) {
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(params.COUCH_URL);
  try {
    return new Promise((resolve, reject) => {
      cloudant
        .postAllDocs({ db: "reviews", includeDocs: true, limit: 100 })
        .then((result) => {
          let reviews = result.result.rows.map((review) => {
            return {
              id: review.doc.id,
              name: review.doc.name,
              dealership: review.doc.dealership,
              review: review.doc.review,
              purchase: review.doc.purchase,
              purchase_date: review.doc.purchase_date,
              car_make: review.doc.car_make,
              car_model: review.doc.car_model,
              car_year: review.doc.car_year,
            };
          });
          if (params.state) {
            reviews = reviews.filter((review) => {
              return review.dealership === params.dealerId;
            });
          }
          resolve({ reviews });
        })
        .catch((err) => {
          console.log(err);
          reject({ err: err });
        });
    });
  } catch (error) {
    return { error: error.description };
  }
}
