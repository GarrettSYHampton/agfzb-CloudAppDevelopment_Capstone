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
        .postAllDocs({ db: "dealerships", includeDocs: true, limit: 100 })
        .then((result) => {
          let dealerships = result.result.rows.map((dealership) => {
            return {
              id: dealership.doc.id,
              city: dealership.doc.city,
              state: dealership.doc.state,
              st: dealership.doc.st,
              address: dealership.doc.address,
              zip: dealership.doc.zip,
              lat: dealership.doc.lat,
              long: dealership.doc.long,
              short_name: dealership.doc.short_name,
              full_name: dealership.doc.full_name,
            };
          });
          if (params.state) {
            dealerships = dealerships.filter((dealership) => {
              return (
                dealership.state.toLowerCase() === params.state.toLowerCase()
              );
            });
          }
          resolve({ dealerships });
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
